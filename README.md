# Automated Refactoring Workflow with n8n, LLM, RAG, and Qdrant

An automated software maintainability analysis and refactoring workflow built with **n8n**, **SonarQube**, **Large Language Models (LLM)**, **Retrieval-Augmented Generation (RAG)**, and **Qdrant**.

This project was developed as part of an undergraduate thesis focused on evaluating and improving software maintainability based on **ISO/IEC 25010**.

---

## Overview

This project implements an automated workflow for processing software maintainability issues identified by SonarQube and generating context-aware refactoring recommendations using an LLM.

The workflow is orchestrated using **n8n** and integrates static analysis results, source-code context, a software engineering knowledge base, and LLM-based analysis.

The general process is:

```text
SonarQube Analysis
        │
        ▼
   SonarQube JSON
        │
        ▼
     n8n Workflow
        │
        ├── Extract Issues
        │
        ├── Group Issues by File
        │
        ├── Read Source Code
        │
        ├── Analyzer Agent
        │
        ├── RAG Retrieval
        │       │
        │       ▼
        │     Qdrant
        │
        ├── Refactoring Recommendation
        │
        └── Validation
                │
                ▼
          Final Result
```

---

## Objectives

The main objectives of this project are:

* Automate the processing of SonarQube maintainability issues.
* Provide source-code context to the LLM during analysis.
* Retrieve relevant software engineering knowledge using RAG.
* Generate context-aware refactoring recommendations.
* Validate generated results before they are applied to source code.
* Reduce repetitive manual work during software maintainability analysis.

---

## Technology Stack

| Component               | Technology                     |
| ----------------------- | ------------------------------ |
| Workflow Orchestration  | n8n                            |
| Static Code Analysis    | SonarQube                      |
| Large Language Model    | LLM                            |
| RAG                     | Retrieval-Augmented Generation |
| Vector Database         | Qdrant                         |
| RAG Framework           | LangChain                      |
| Containerization        | Docker                         |
| Container Orchestration | Docker Compose                 |
| Programming Language    | Python, JavaScript             |
| Data Format             | JSON                           |

---

## Project Structure

```text
.
├── .gitignore
├── docker-compose.yml
├── python_fetch_sonarqube.py
├── README.md
│
├── n8nvolume/
│   ├── PersisApps/
│   └── Knowledge_base/
│
└── workflow/
    ├── AutomatedRefactorWorkflown8n.json
    └── Knowledge Base Ingestion - Qdrant.json
```

### Description

#### `docker-compose.yml`

Docker Compose configuration used to run:

* n8n
* Qdrant

#### `python_fetch_sonarqube.py`

Python script used to retrieve or process SonarQube analysis data for the workflow.

#### `workflow/`

Contains the exported n8n workflows.

**`AutomatedRefactorWorkflown8n.json`**

Main workflow for automated maintainability analysis and refactoring.

**`Knowledge Base Ingestion - Qdrant.json`**

Workflow used to process the knowledge base and store its vector representations in Qdrant.

#### `n8nvolume/`

Local directory used by Docker as a host-mounted volume.

This directory is **not included in the Git repository**.

It contains local resources required by the workflow, including:

* `YourApps/`
* `Knowledge_base/`

---

## Workflow Components

### 1. SonarQube Analysis

SonarQube is used to perform static analysis of the application source code.

The analysis produces information such as:

* Code smells
* Complexity
* Bugs
* Duplications
* Issue severity
* Issue location
* SonarQube rule information

The analysis result is processed in JSON format.

---

### 2. Issue Processing

The n8n workflow extracts individual SonarQube issues from the JSON result.

Issues are grouped according to their affected source files so that the LLM can analyze each issue together with the corresponding source-code context.

---

### 3. Source Code Context

The workflow retrieves the source code associated with the detected SonarQube issue.

The source-code context is provided to the analysis process together with:

* File path
* Issue message
* SonarQube rule
* Issue severity
* Line number
* Surrounding source-code lines

This allows the LLM to analyze the issue based on the actual implementation rather than the SonarQube message alone.

---

### 4. Analyzer Agent

The Analyzer Agent analyzes the detected issue and determines the relevant maintainability problem based on:

* SonarQube rule
* Issue message
* Source-code context
* Issue location

The analysis is then passed to the RAG component for additional software engineering context.

---

### 5. RAG Agent

The RAG component retrieves relevant information from the software engineering knowledge base.

The knowledge base contains references related to:

* Clean Code
* SOLID Principles
* Design Patterns
* Refactoring Patterns
* Software Maintainability

The retrieval process is:

```text
Knowledge Base
      │
      ▼
Document Chunking
      │
      ▼
Embedding
      │
      ▼
Qdrant
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
LLM
```

---

### 6. Refactoring Recommendation

The LLM uses the SonarQube issue, source-code context, and retrieved knowledge to generate a refactoring recommendation.

The recommendation is intended to improve characteristics related to software maintainability while preserving the intended behavior of the source code.

---

### 7. Validation

The generated result is passed through validation before being considered a final output.

The validation process checks aspects such as:

* Output structure
* Syntax-related constraints
* Placeholder detection
* Refactoring consistency
* Maintainability considerations

The generated recommendation should still be reviewed by a developer before being applied to production source code.

---

## Docker Services

The project uses Docker Compose to run two primary services.

### n8n

n8n is used as the workflow orchestration platform.

Default URL:

```text
http://localhost:5678
```

### Qdrant

Qdrant is used as the vector database for storing and retrieving knowledge-base embeddings.

Default URL:

```text
http://localhost:6333
```

---

## Requirements

Before running the project, install:

* Docker Desktop
* Docker Compose
* Python 3.13.5
* Git

The project also requires the credentials/API access required by the configured LLM and embedding services.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<username>/<repository>.git
```

Navigate to the project directory:

```bash
cd <repository>
```

---

### 2. Prepare the Local Directory

The project requires local directories that are intentionally excluded from Git.

Create the required directories:

```text
n8nvolume/
├── PersisApps/
└── Knowledge_base/
```

The `PersisApps` directory must contain the authorized local copy of the application source code used as the research object.

> The source code of the research object is not distributed through this repository.

---

### 3. Create the Docker Volume

The n8n service uses an external Docker volume named:

```text
n8n_data
```

Create it with:

```bash
docker volume create n8n_data
```

---

### 4. Start the Services

Run:

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
n8n
qdrant
```

---

## Import n8n Workflows

After the containers are running, open:

```text
http://localhost:5678
```

Import the workflow files located in:

```text
workflow/
```

Import:

```text
AutomatedRefactorWorkflown8n.json
```

and:

```text
Knowledge Base Ingestion - Qdrant.json
```

After importing the workflows, configure the required credentials and service connections.

---

## Knowledge Base Ingestion

The knowledge-base workflow is responsible for preparing software engineering references for RAG retrieval.

The general process is:

```text
Knowledge Documents
        │
        ▼
     Chunking
        │
        ▼
    Embedding
        │
        ▼
     Qdrant
        │
        ▼
 Vector Similarity Search
```

The resulting vectors are stored in Qdrant and can subsequently be retrieved by the automated refactoring workflow.

---

## Configuration

Sensitive credentials must not be committed to Git.

Do not upload:

* API keys
* Access tokens
* Passwords
* LLM credentials
* Embedding credentials
* n8n credentials
* `N8N_ENCRYPTION_KEY`
* Private source code
* Database files
* Docker runtime data

Credentials should be configured locally through n8n or the appropriate environment configuration.

---

## External Research Source

The workflow uses an external application source code as the research object.

The source code is intentionally **not included in this repository** because it belongs to an external party and is not intended for public distribution.

The Docker Compose configuration mounts the source code from a local host directory:

```yaml
- C:/project_satria/docker/n8nvolume/PersisApps:/home/node/.n8n-files/PersisApps
```

The local path may need to be modified according to the environment where the project is executed.

The source code should only be used with appropriate authorization.

---

## Data and Runtime Files

The following resources are intentionally excluded from Git:

```text
n8nvolume/
qdrant_storage/
n8n_data
```

These resources contain local application data, runtime data, vector database data, or external research resources.

The Git repository therefore contains the **workflow and configuration required to reproduce the research process**, rather than private application data or runtime state.

---

## Research Context

This project was developed as part of an undergraduate thesis entitled:

> **Evaluasi Maintainability Aplikasi PPDB MA Persis Kudang Menggunakan LLM, SCAT, dan Manual Review Berdasarkan ISO/IEC 25010**

The research combines several approaches to evaluate and improve software maintainability:

1. Static analysis using SonarQube.
2. LLM-based source-code analysis.
3. Retrieval-Augmented Generation.
4. Automated refactoring recommendations.
5. Manual review.
6. Human validation.

The automation developed in this repository focuses on the implementation of the LLM, RAG, and workflow orchestration components.

---

## Disclaimer

The generated analysis and refactoring recommendations are produced with the assistance of an LLM.

The output should not be considered an automatic replacement for developer review.

Before applying any generated refactoring to a production system, the proposed changes should be reviewed, tested, and validated by a qualified developer.

---

## License

This repository is intended primarily for academic and research purposes.

The source code of the external application used as the research object is not included in this repository.

If this repository is later distributed as an open-source project, an appropriate license should be added here.
