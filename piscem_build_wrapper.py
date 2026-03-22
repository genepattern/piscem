#!/usr/bin/env python3
"""
Wrapper script for piscem.build GenePattern module.
Indexes one or more reference sequences using piscem, building a compacted colored de Bruijn graph and sshash data structure.
"""

import argparse
import sys
import os
import subprocess
import logging
import resource
import tarfile
import glob
from pathlib import Path


def setup_logging(verbose=False):
    """Configure logging for the wrapper."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description='piscem.build wrapper for GenePattern'
    )

    parser.add_argument('--reference-files', required=True, help='Reference FASTA files to index')
    parser.add_argument('--kmer-length', required=True, type=int, help='Length of the k-mer to use')
    parser.add_argument('--minimizer-length', required=True, type=int, help='Length of the minimizer to use')
    parser.add_argument('--threads', required=True, type=int, help='Number of threads to use')
    parser.add_argument('--output', required=True, help='Output file stem/prefix')
    parser.add_argument('--work-dir', help='Working directory')
    parser.add_argument('--keep-intermediate-dbg', action='store_true', help='Keep intermediate de Bruijn graph files')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--no-ec-table', action='store_true', help='Skip equivalence class table construction')
    parser.add_argument('--seed', type=int, help='Random seed')

    return parser.parse_args()


def validate_inputs(args):
    """Validate input parameters and files."""
    # Check if reference files exist
    if not os.path.exists(args.reference_files):
        logging.error(f"Reference file does not exist: {args.reference_files}")
        return False
    
    # Validate k-mer length
    if args.kmer_length < 15 or args.kmer_length > 63 or args.kmer_length % 2 == 0:
        logging.error("K-mer length must be odd and between 15-63")
        return False
    
    # Validate minimizer length
    if args.minimizer_length >= args.kmer_length:
        logging.error("Minimizer length must be smaller than k-mer length")
        return False
    
    return True


def create_output_tarball(output_prefix):
    """Package all generated index files into a tarball."""
    tarball_name = f"{output_prefix}_piscem_index.tar.gz"
    
    # Find all files with the output prefix
    index_files = glob.glob(f"{output_prefix}*")
    
    if not index_files:
        logging.error(f"No index files found with prefix {output_prefix}")
        return False
    
    try:
        with tarfile.open(tarball_name, 'w:gz') as tar:
            for file_path in index_files:
                tar.add(file_path, arcname=os.path.basename(file_path))
                logging.info(f"Added {file_path} to tarball")
        
        logging.info(f"Created tarball: {tarball_name}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to create tarball: {e}")
        return False


def run_tool(args):
    """Execute piscem build with validated parameters."""
    # Set file handle limit before running piscem
    resource.setrlimit(resource.RLIMIT_NOFILE, (2048, 2048))
    
    # Construct the command
    cmd = ['piscem', 'build']
    cmd.extend(['-s', args.reference_files])  # Map --reference-files to -s
    cmd.extend(['-k', str(args.kmer_length)])
    cmd.extend(['-m', str(args.minimizer_length)])
    cmd.extend(['-t', str(args.threads)])
    cmd.extend(['-o', args.output])
    
    if args.work_dir:
        cmd.extend(['-w', args.work_dir])
    if args.keep_intermediate_dbg:
        cmd.append('--keep-intermediate-dbg')
    if args.overwrite:
        cmd.append('--overwrite')
    if args.no_ec_table:
        cmd.append('--no-ec-table')
    if args.seed:
        cmd.extend(['--seed', str(args.seed)])

    logging.info(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        if result.stdout:
            logging.info(f"Tool output: {result.stdout}")

        logging.info("piscem build completed successfully")
        
        # Create output tarball
        if not create_output_tarball(args.output):
            return False
        
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"piscem build failed with exit code {e.returncode}")
        if e.stderr:
            logging.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False


def main():
    """Main entry point for the wrapper script."""
    args = parse_arguments()
    setup_logging()

    try:
        # Validate inputs
        if not validate_inputs(args):
            logging.error("Input validation failed")
            sys.exit(1)

        # Run the tool
        success = run_tool(args)
        sys.exit(0 if success else 1)

    except Exception as e:
        logging.error(f"Wrapper execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()