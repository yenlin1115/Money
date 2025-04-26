[繁體中文](README-zh-tw.md)
# AI MCP Dashboard

## Overview
This project implements an AI-powered Market Control Panel (MCP) dashboard that leverages artificial intelligence to provide enhanced market insights and trading analytics. The dashboard combines market data with advanced AI algorithms to deliver real-time market analysis and predictive insights.

## Features
- Real-time market data integration
- AI-powered market trend analysis and predictions
- Interactive data visualization and charting
- Stock price prediction using machine learning
- Portfolio tracking and analysis
- Historical data analysis
- Trading agent integration

## Technology Stack
- Python 3.x
- Django Web Framework
- Machine Learning Libraries:
  - scikit-learn
  - pandas
  - numpy
- Data Visualization:
  - Plotly
  - Matplotlib
- OpenAI API Integration

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

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
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
├── Moneytest/        # Django project configuration
├── companies/        # Stock and company data models and views
├── templates/        # HTML templates
├── data/            # Data storage
├── plots/           # Generated plots
├── trading_agents/  # Trading agent implementations
└── utils/           # Utility functions
```

## Roadmap
- [ ] Enhanced market data sources
- [ ] Advanced trading algorithms
- [ ] Mobile application support
- [ ] Real-time data streaming
- [ ] Portfolio optimization

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions or suggestions, please contact:
- Email: yenlin1115@gmail.com
- GitHub: [@yenlin1115](https://github.com/yenlin1115)

## Acknowledgments
- Contributors and maintainers of the open-source libraries used in this project 