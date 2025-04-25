# AI MCP Bloomberg Dashboard

## Overview
This project implements an AI-powered Market Control Panel (MCP) Bloomberg dashboard that leverages artificial intelligence to provide enhanced market insights and trading analytics. The dashboard combines Bloomberg terminal data with advanced AI algorithms to deliver real-time market analysis and predictive insights.

## Features
- Real-time market data integration with Bloomberg Terminal
- AI-powered market trend analysis and predictions
- Interactive data visualization and charting
- Custom alert system for market movements
- Portfolio optimization recommendations
- Risk assessment metrics
- Historical data analysis

## Technology Stack
- Python 3.x
- Bloomberg API (blpapi)
- Machine Learning Libraries:
  - TensorFlow/PyTorch
  - scikit-learn
  - pandas
- Data Visualization:
  - Plotly
  - Dash
- Web Framework:
  - FastAPI
  - Django

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yenlin1115/Money.git
cd Money
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Bloomberg API credentials in `.env` file:
```
BLOOMBERG_API_HOST=your_host
BLOOMBERG_API_PORT=your_port
BLOOMBERG_API_KEY=your_key
```

## Usage
1. Start the dashboard server:
```bash
python manage.py runserver
```

2. Access the dashboard at `http://localhost:8000`

## Project Structure
```
Money/
├── api/              # API endpoints and Bloomberg data integration
├── dashboard/        # Dashboard UI components
├── ml_models/        # Machine learning models and algorithms
├── utils/           # Utility functions and helpers
├── tests/           # Test suite
└── config/          # Configuration files
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or suggestions, please contact:
- Email: yenlin1115@gmail.com
- GitHub: [@yenlin1115](https://github.com/yenlin1115)

## Acknowledgments
- Bloomberg L.P. for providing the Bloomberg API
- Contributors and maintainers of the open-source libraries used in this project 