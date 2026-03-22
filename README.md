# piscem.build (v0.16.2)

**Description**: Indexes one or more reference sequences using piscem, building a compacted colored de Bruijn graph and sshash data structure
**Authors**: Rob Patro; University of Maryland, College Park
**Contact**: gp-help@broadinstitute.org
**Algorithm Version**: 0.16.2

## Summary

The piscem.build module creates high-performance indices for RNA-seq quantification using the piscem framework. This module wraps the `piscem build` command to construct a compacted colored de Bruijn graph and sshash data structure from reference transcriptome sequences. The resulting index enables ultra-fast mapping and quantification of RNA-seq reads.

piscem is designed for efficient single-cell RNA-seq analysis but also works well for bulk RNA-seq. The indexing process builds a minimizer-based data structure that allows for rapid k-mer lookups during the mapping phase. This module produces a compressed archive containing all necessary index files that can be used with piscem mapping modules.

## References

1. Almodaresi, F., Sarkar, H., Srivastava, A., & Patro, R. (2018). A space and time-efficient index for the compacted colored de Bruijn graph. Bioinformatics, 34(13), i169-i177.
2. He, D., Zakeri, M., Sarkar, H., Soneson, C., Srivastava, A., & Patro, R. (2022). Alevin-fry unlocks rapid, accurate and memory-frugal quantification of single-cell RNA-seq data. Nature Methods, 19(3), 316-322.

## Source Links

* [piscem GitHub Repository](https://github.com/COMBINE-lab/piscem)
* [Docker Hub](https://hub.docker.com/r/genepattern/piscem-build)
* [Dockerfile](https://github.com/genepattern/piscem-build-gp/blob/main/Dockerfile)

## Parameters

| Name | Description | Default Value |
| :--- | :--- | :--- |
| reference.files * | Reference FASTA files to index | |
| kmer.length * | Length of the k-mer to use | 31 |
| minimizer.length * | Length of the minimizer to use | 19 |
| threads * | Number of threads to use | 1 |
| output.prefix * | Output file stem/prefix | piscem_index |
| work.dir | Working directory for intermediate files | |
| keep.intermediate.dbg | Preserve intermediate de Bruijn graph files | false |
| overwrite | Overwrite existing output files | false |
| no.ec.table | Skip equivalence class table construction | false |
| seed | Random seed for reproducible results | |

\* required

## Input Files

1. **reference.files**
   
   Reference transcriptome sequences in FASTA format (.fa, .fasta, .fa.gz, .fasta.gz). Can be a single file or comma-separated list of files. For single-cell analysis, typically use a transcriptome FASTA from Ensembl, GENCODE, or RefSeq. For bulk RNA-seq, can also use genome sequences with appropriate gene annotations.
   
   **Format Requirements:**
   - FASTA format with standard extensions
   - Gzip compression supported
   - Sequence headers should be unique
   - No special characters in sequence names recommended

## Output Files

1. **{output.prefix}_piscem_index.tar.gz**
   
   Compressed archive containing the complete piscem index structure. This includes the compacted colored de Bruijn graph, sshash data structure, equivalence class tables (if generated), and metadata files. The archive can be directly used as input for piscem mapping modules.
   
   **Contents:**
   - Binary index files (.sshash, .ctg, .pos)
   - Equivalence class mapping tables
   - Reference sequence metadata
   - Index construction parameters

## Example Data

Input:
[Link to example transcriptome FASTA file - typically Homo_sapiens.GRCh38.cdna.all.fa.gz]

Output:
[Link to example piscem index archive - piscem_index_piscem_index.tar.gz]

## Requirements

- **Memory**: 8-32 GB RAM depending on reference size (human transcriptome ~16 GB)
- **Storage**: 3-5x reference file size for temporary files
- **CPU**: Multi-threading supported, performance scales with core count
- **Docker Image**: genepattern/piscem-build:0.16.2
- **Base Image**: Ubuntu 20.04 with Miniconda3
- **Dependencies**: piscem v0.16.2 installed via bioconda

## License

MIT License - See [piscem repository](https://github.com/COMBINE-lab/piscem/blob/main/LICENSE) for full license text.

## Version Comments

| Version | Release Date | Description |
| :--- | :--- | :--- |
| 0.16.2 | 2024-01-15 | Initial GenePattern module release with piscem 0.16.2, supports standard transcriptome indexing with optimized parameters |