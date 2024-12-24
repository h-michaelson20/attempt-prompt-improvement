def load_css():
    return """
        /* Modern color palette */
        :root {
            --primary-color: #1f2937;
            --secondary-color: #3b82f6;
            --accent-color: #60a5fa;
            --background-color: #f3f4f6;
            --surface-color: #ffffff;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --success-color: #059669;
            --error-color: #dc2626;
        }

        /* Global styles */
        .stApp {
            background-color: var(--background-color);
        }

        /* Card-like containers */
        div[data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: 700;
            color: var(--primary-color);
            background: var(--surface-color);
            padding: 0.5rem;
            border-radius: 8px;
        }
        
        div[data-testid="stMetricDelta"] > div {
            font-size: 16px;
            font-weight: 500;
        }

        /* Headers */
        .main-header {
            font-size: 42px;
            font-weight: 800;
            color: var(--primary-color);
            padding: 2rem 0;
            text-align: center;
            background: linear-gradient(135deg, #f0f2f6, #ffffff);
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        .section-header {
            font-size: 28px;
            font-weight: 600;
            color: var(--primary-color);
            padding: 1rem 0;
            margin: 1.5rem 0;
            border-bottom: 3px solid var(--accent-color);
            background: linear-gradient(90deg, var(--accent-color) 0%, transparent 100%);
            background-clip: text;
            -webkit-background-clip: text;
        }

        /* Containers */
        .metric-container {
            background: var(--surface-color);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin: 1rem 0;
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out;
        }
        
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.1), 0 4px 6px -1px rgba(0, 0, 0, 0.06);
        }

        /* Cost breakdown section */
        .cost-breakdown {
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid rgba(59, 130, 246, 0.1);
        }

        /* Model selection area */
        .model-select {
            background: var(--surface-color);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 2px solid var(--accent-color);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        /* Info boxes */
        .info-box {
            background: linear-gradient(135deg, #e7f1ff, #f0f7ff);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 6px solid var(--secondary-color);
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        /* Streamlit elements customization */
        .stSelectbox {
            background: var(--surface-color);
            border-radius: 8px;
            border: 1px solid var(--accent-color);
        }

        .stSlider {
            padding: 1rem 0;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: var(--surface-color);
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        /* Number input styling */
        .stNumberInput {
            background: var(--surface-color);
            border-radius: 8px;
            border: 1px solid var(--accent-color);
        }

        /* Custom classes for specific elements */
        .cost-metric {
            font-size: 24px;
            font-weight: 600;
            color: var(--primary-color);
            padding: 1rem;
            background: linear-gradient(135deg, #f0f2f6, #ffffff);
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            margin: 0.5rem 0;
        }

        .highlight-box {
            background: linear-gradient(135deg, #f0f7ff, #ffffff);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--accent-color);
            margin: 0.5rem 0;
        }

        /* Tooltip customization */
        div[data-baseweb="tooltip"] {
            background: var(--primary-color);
            border-radius: 6px;
            padding: 0.5rem;
            font-size: 14px;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--background-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary-color);
        }
    """ 