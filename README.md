# Clinical Note Extraction

## Description
The **Clinical-Note-Extraction** repository provides a machine learning pipeline designed to extract structured medical information from unstructured clinical notes. Leveraging PyTorch and Hugging Face Transformers, it includes modules for data preprocessing, model definition, and dedicated training scripts for classifying or extracting both diagnoses and medical procedures from text data.

## Folder Structure

```text
Clinical-Note-Extraction/
├── data/                  # Directory for storing input datasets and clinical notes (e.g., CSV files).
├── models/                # Directory for saving trained model weights and checkpoints.
├── modules/               # Core machine learning and processing scripts.
│   ├── diagnosis_training.py  # Script for training the diagnosis extraction model.
│   ├── procedure_training.py  # Script for training the procedure extraction model.
│   ├── models.py              # PyTorch and Transformer model architectures.
│   └── processing/            # Data preprocessing scripts.
│       ├── process_csv.py     # Utilities for handling and formatting CSV data files.
│       └── processing.py      # General data processing, tokenization, and cleaning functions.
├── shared_functions/      # Reusable utility and helper functions.
│   ├── gg_sheet_drive.py      # Helper functions for Google Sheets and Google Drive integration.
│   └── global_functions.py    # Commonly used utility functions across the pipeline.
└── requirements.txt       # Python dependencies required to run the project.
```

## Setup Manual

### 1. Clone the repository
First, clone the repository to your local machine and navigate to the project directory:
```bash
git clone <repository_url>
cd Clinical-Note-Extraction
```

### 2. Set up a Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to manage your dependencies and avoid conflicts.
```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages using the provided `requirements.txt` file. This will install necessary libraries such as `torch`, `transformers`, `pandas`, and `scikit-learn`.
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Since the project uses `python-dotenv`, you may need to configure environment variables (e.g., for Google Drive API keys or database connections). 
- Create a `.env` file in the root directory.
- Add your specific environment variables to this file.

### 5. Prepare the Data
Place your clinical text datasets (e.g., CSV files containing the clinical notes) into the `data/` directory. Ensure your data formats align with the expectations of the scripts in `modules/processing/`.

Script to get specific file from the Data repo on Huggingface: 

```bash
curl -L -H "Authorization: Bearer hf_token_here" https://huggingface.co/datasets/zinzinmit/Note/resolve/main/file -o target_path
```

Or pull the whole repo and git lfs later 
```shell
$env:GIT_LFS_SKIP_SMUDGE=1; git clone https://huggingface.co/datasets/zinzinmit/Note
```

### 6. Run the Pipeline
You can now start training the models using the scripts provided in the `modules/` directory.

For example, to train the procedure extraction model:
```bash
python modules/procedure_training.py
```

To train the diagnosis extraction model:
```bash
python modules/diagnosis_training.py
```
*(Note: Be sure to verify the specific arguments or configuration required by these training scripts by checking the source code).*
