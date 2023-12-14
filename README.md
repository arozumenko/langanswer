# langanswer
Experiment with langchain based embeddings

## Installation

1. Create a virtual environment `python3 -m venv venv`
2. Activate the virtual environment `source venv/bin/activate`
3. Install the requirements `pip install -r requirements.txt`
4. Create `nltk_data` directory `mkdir nltk_data`
5. Create `chroma` directory `mkdir chroma`
6. Fill `.env` file with your appropriate values for LLM and embeddings connections


## Usage
Run `streamlit run ui.py` and open the link in your browser
Some depencencies might be missing, install them with `pip install <dependency>`

## Examples:

### Directory Loader
Loader Params:
```json
{
  "path": "./data",
  "use_multithreading": false,
  "loader_cls": "TextLoader",
  "table_raw_content": true,
  "docs_page_split": true
}
```

Load params:
```json
{}
```

### Confluence Loader
Loader Params:
```json
{
    "url": "https://yoursite.atlassian.com/wiki",
    "token": "Your API Token for confluence",
    "cloud": false | true
}
```

Load params:
```json
{
    "space_key": "SOMESPACE",
    "limit": 50,
    "max_pages": 1000,
    "content_format": "view" | "storage" | "anonymous" | "editor"
}
```

### Git Repo Loader
Loader Params:
```json
{
    "source": "https://github.com/arozumenko/langanswer.git",
    "branch": "main",
    "username": "your git username",
    "password": "your git api token",
    "use_multithreading": false,
    "loader_cls": "TextLoader",
    "index_file_exts": ".py, .txt"
}
```

loader_cls is a fallback class in case document was not qualified for any of the available classes.

Load params:
```json
{}
```
