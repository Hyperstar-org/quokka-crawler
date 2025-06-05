# TikTok Crawler Actor

A powerful TikTok influencer crawler built with the Apify SDK, designed to extract TikTok influencer data based on keywords. This actor is containerized with Docker and uses Poetry for dependency management.

## 🚀 Features

- **Keyword-based Search**: Search for TikTok influencers using hashtags
- **Configurable Limits**: Set maximum number of influencers to extract
- **Apify Integration**: Built on the robust Apify platform for web scraping
- **Docker Support**: Fully containerized for easy deployment
- **Modern Python**: Uses Python 3.11 with async/await patterns

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Poetry (for local development)

## 🛠️ Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <your-repo-url>
cd tiktok-actor
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

### Local Development with Poetry

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Run the actor:
```bash
python main.py
```

## 🔧 Configuration

The actor accepts the following input parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keyword` | string | `k-beauty` | The keyword to search for (hashtag will be automatically added) |
| `max_influencers` | integer | `50` | Maximum number of influencers to extract |

### Input Example

```json
{
  "keyword": "fashion",
  "max_influencers": 100
}
```

## 🏃‍♂️ Usage

### Running with Apify CLI

```bash
apify run
```

### Running with Custom Input

Create an `INPUT.json` file in the project root:

```json
{
  "keyword": "fitness",
  "max_influencers": 75
}
```

Then run:
```bash
python main.py
```

### Using Docker with Custom Input

You can pass environment variables or mount a volume with your input file:

```bash
docker run -v $(pwd)/INPUT.json:/app/INPUT.json your-image-name
```

## 📁 Project Structure

```
tiktok-actor/
├── main.py                 # Main entry point
├── components/             
│   ├── helpers.py          # Utility functions and logger
│   └── scraper.py          # TikTok scraper implementation
├── pyproject.toml          # Poetry configuration and dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose setup
├── poetry.lock            # Locked dependency versions
└── README.md              # This file
```

## 🔍 How It Works

1. **Initialization**: The actor initializes with the Apify SDK and opens a dataset named "tiktok"
2. **Input Processing**: Reads keyword and max_influencers from actor input
3. **Hashtag Formation**: Automatically adds "#" prefix to the keyword
4. **Scraping**: Uses the TikTokScraper class to extract influencer data
5. **Data Storage**: Stores results in the Apify dataset for easy access

## 📦 Dependencies

- **apify**: Apify SDK for Python
- **beautifulsoup4**: HTML parsing library
- **httpx**: Modern HTTP client for Python
- **python-decouple**: Configuration management
- **lxml**: XML/HTML processing library

## 🐳 Docker Details

The Docker setup includes:
- Python 3.11 slim base image
- System dependencies for XML processing
- Poetry installation and configuration
- Automatic dependency installation
- Non-root virtualenv configuration

## 📊 Output

The crawler stores extracted data in an Apify dataset with the name "tiktok". The data can be accessed through:
- Apify Console
- Apify API
- Local dataset files (when running locally)

## 🔧 Development

### Adding New Features

1. Modify the `TikTokScraper` class in `components/scraper.py`
2. Update input parameters in `main.py` if needed
3. Add new dependencies to `pyproject.toml`
4. Rebuild the Docker image

### Debugging

Enable verbose logging by modifying the logger configuration in `components/helpers.py`.

## 🚀 Deployment

### Apify Platform

1. Push your code to a Git repository
2. Create a new Actor on Apify Console
3. Connect your repository
4. Configure build settings
5. Deploy and run

### Self-hosted

Use the provided Docker configuration to deploy on any container platform:

```bash
docker build -t tiktok-crawler .
docker run tiktok-crawler
```

## 📝 License

This project uses a custom license as specified in `pyproject.toml`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the Apify documentation: https://docs.apify.com/sdk/python
- Review the project's issue tracker
- Contact the maintainer: sang721

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please ensure you comply with TikTok's Terms of Service and robots.txt when using this crawler. Be respectful of rate limits and consider the impact of your scraping activities.