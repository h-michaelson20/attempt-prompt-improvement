import streamlit as st
import pandas as pd
from src.data_loader import load_excel_data, get_numeric_columns, get_categorical_columns
from src.visualizations import create_histogram, create_bar_chart, create_scatter_plot
from src.cost_calculator import LLMCostCalculator
from src.token_calculator import estimate_tokens
from src.styles import load_css

# Page config
st.set_page_config(
    page_title="LLM Cost Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load and inject CSS
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# Load data
try:
    df = load_excel_data()
    cost_calculator = LLMCostCalculator(df)
    
    # Main navigation
    st.markdown('<div class="main-header">LLM Cost Analysis Dashboard</div>', unsafe_allow_html=True)
    analysis_type = st.sidebar.radio(
        "Choose Analysis Type",
        ["Single Model Simulator", "Model Comparison", "Cost Visualization"]
    )
    
    if analysis_type == "Single Model Simulator":
        # Original single model calculator
        st.subheader("Single Model Cost Simulator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_column = cost_calculator.model_column
            selected_model = st.selectbox(
                "Select LLM Model:",
                df[model_column].unique()
            )
            
            st.write("### Input Message")
            user_input = st.text_area(
                "Enter your message:",
                height=150,
                key="input_text_single",
            )
            
            input_tokens = estimate_tokens(user_input)
            estimated_output = int(input_tokens * 2) if 'gpt-4' in selected_model.lower() else int(input_tokens * 1.5)
            
            st.write("### Token Estimates")
            token_col1, token_col2 = st.columns(2)
            with token_col1:
                st.metric("Input Tokens", input_tokens)
            with token_col2:
                output_tokens = st.number_input(
                    "Expected Output Tokens:",
                    value=estimated_output,
                    key="output_tokens_single"
                )
            
            costs = cost_calculator.calculate_cost(selected_model, input_tokens, output_tokens)
            
            st.write("### 💰 Cost Breakdown")
            cost_cols = st.columns(3)
            with cost_cols[0]:
                st.metric("Input Cost", f"${costs['input_cost']:.4f}")
            with cost_cols[1]:
                st.metric("Output Cost", f"${costs['output_cost']:.4f}")
            with cost_cols[2]:
                st.metric("Total Cost", f"${costs['total_cost']:.4f}")
    
    elif analysis_type == "Model Comparison":
        st.subheader("Model Strategy Comparison")
        
        comparison_type = st.radio(
            "What would you like to compare?",
            ["Single vs Single Model", "Single vs Multi-Model Strategy", "Compare Multi-Model Strategies"],
            help="Choose how you want to compare different model strategies"
        )
        
        # Usage Pattern Inputs (shared across all comparisons)
        st.write("### Daily Usage Patterns")
        usage_col1, usage_col2 = st.columns(2)
        with usage_col1:
            queries_per_day = st.number_input(
                "Number of Queries per Day",
                min_value=1,
                value=100
            )
            avg_input_tokens = st.number_input(
                "Average Input Tokens per Query",
                min_value=1,
                value=500
            )
        with usage_col2:
            avg_output_ratio = st.slider(
                "Average Output/Input Token Ratio",
                min_value=0.5,
                max_value=3.0,
                value=1.5,
                step=0.1
            )
        
        # Different comparison views based on selection
        if comparison_type == "Single vs Single Model":
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Model A")
                model_a = st.selectbox(
                    "Select First Model:",
                    df[cost_calculator.model_column].unique(),
                    key="model_a"
                )
                costs_a = cost_calculator.calculate_cost(
                    model_a,
                    avg_input_tokens * queries_per_day,
                    int(avg_input_tokens * avg_output_ratio) * queries_per_day
                )
                
                st.metric("Daily Cost", f"${costs_a['total_cost']:,.2f}")
                st.metric("Annual Cost", f"${(costs_a['total_cost'] * 365):,.2f}")
                st.metric("Cost per Query", f"${(costs_a['total_cost'] / queries_per_day):,.4f}")
                
            with col2:
                st.write("### Model B")
                model_b = st.selectbox(
                    "Select Second Model:",
                    df[cost_calculator.model_column].unique(),
                    key="model_b"
                )
                costs_b = cost_calculator.calculate_cost(
                    model_b,
                    avg_input_tokens * queries_per_day,
                    int(avg_input_tokens * avg_output_ratio) * queries_per_day
                )
                
                # Calculate cost difference for delta display
                cost_difference = costs_a['total_cost'] - costs_b['total_cost']
                cost_difference_pct = (cost_difference / costs_a['total_cost']) * 100
                
                # Format delta string with appropriate sign
                if cost_difference >= 0:
                    delta_str = f"${abs(cost_difference):,.2f} ({abs(cost_difference_pct):.1f}%)"
                else:
                    delta_str = f"-${abs(cost_difference):,.2f} (-{abs(cost_difference_pct):.1f}%)"
                
                st.metric(
                    "Daily Cost",
                    f"${costs_b['total_cost']:,.2f}",
                    delta_str if cost_difference >= 0 else f"-{delta_str.lstrip('-')}",
                    delta_color="normal" if cost_difference >= 0 else "inverse"
                )
                st.metric("Annual Cost", f"${(costs_b['total_cost'] * 365):,.2f}")
                st.metric("Cost per Query", f"${(costs_b['total_cost'] / queries_per_day):,.4f}")
                
        elif comparison_type == "Single vs Multi-Model Strategy":
            single_col, multi_col = st.columns(2)
            
            with single_col:
                st.write("### Single Model Approach")
                single_model = st.selectbox(
                    "Select Model:",
                    df[cost_calculator.model_column].unique(),
                    key="single_model_comparison"
                )
                
                # Calculate single model daily costs
                single_daily_cost = cost_calculator.calculate_cost(
                    single_model,
                    avg_input_tokens * queries_per_day,
                    int(avg_input_tokens * avg_output_ratio) * queries_per_day
                )
                
                st.metric(
                    "Daily Cost",
                    f"${single_daily_cost['total_cost']:,.2f}"
                )
                
                st.metric(
                    "Projected Annual Cost",
                    f"${(single_daily_cost['total_cost'] * 365):,.2f}",
                    help="Projected annual cost (365 days)"
                )
                
                st.metric(
                    "Cost per Query",
                    f"${(single_daily_cost['total_cost'] / queries_per_day):,.4f}",
                    help="Average cost per query"
                )
            
            with multi_col:
                st.write("### Multi-Model Strategy")
                
                # Classifier model selection
                classifier_model = st.selectbox(
                    "Query Classification Model:",
                    df[cost_calculator.model_column].unique(),
                    key="classifier_model",
                    help="Model used to classify and route queries"
                )
                
                num_models = st.number_input(
                    "Number of Models",
                    min_value=2,
                    max_value=5,
                    value=2,
                    key="multi_model_count"
                )
                
                # Model selection and percentages
                models = []
                percentages = []
                total_percentage = 0
                model_costs = []
                
                for i in range(num_models):
                    model = st.selectbox(
                        f"Model {i+1}:",
                        df[cost_calculator.model_column].unique(),
                        key=f"multi_model_{i}"
                    )
                    models.append(model)
                    
                    if i == num_models - 1:
                        percentage = 100 - total_percentage
                        st.write(f"Percentage: {percentage}%")
                    else:
                        percentage = st.slider(
                            f"Percentage for Model {i+1}",
                            0, 100-total_percentage,
                            value=min(50, 100-total_percentage),
                            key=f"multi_percentage_{i}"
                        )
                    percentages.append(percentage)
                    total_percentage += percentage
                    
                    # Calculate costs for each model
                    model_queries = int(queries_per_day * (percentage / 100))
                    model_cost = cost_calculator.calculate_cost(
                        model,
                        avg_input_tokens * queries_per_day,  # Full context for all queries
                        int(avg_input_tokens * avg_output_ratio) * model_queries  # Output only for this model's queries
                    )
                    model_costs.append(model_cost)
                
                # Calculate classification costs
                classifier_daily_cost = cost_calculator.calculate_cost(
                    classifier_model,
                    100 * queries_per_day,  # Assuming 100 tokens per classification
                    50 * queries_per_day  # Assuming 50 tokens output for classification decision
                )
                
                # Calculate total multi-model costs
                total_multi_daily = classifier_daily_cost['total_cost'] + sum(cost['total_cost'] for cost in model_costs)
                
                # Calculate cost difference for delta display
                cost_difference = single_daily_cost['total_cost'] - total_multi_daily
                cost_difference_pct = (cost_difference / single_daily_cost['total_cost']) * 100
                
                # Format delta string with appropriate sign
                if cost_difference >= 0:
                    delta_str = f"${abs(cost_difference):,.2f} ({abs(cost_difference_pct):.1f}%)"
                else:
                    delta_str = f"-${abs(cost_difference):,.2f} (-{abs(cost_difference_pct):.1f}%)"
                
                st.metric(
                    "Daily Cost",
                    f"${total_multi_daily:,.2f}",
                    delta_str if cost_difference >= 0 else f"-{delta_str.lstrip('-')}",
                    delta_color="normal" if cost_difference >= 0 else "inverse"
                )
                
                st.metric(
                    "Projected Annual Cost",
                    f"${(total_multi_daily * 365):,.2f}",
                    help="Projected annual cost (365 days)"
                )
                
                st.metric(
                    "Cost per Query",
                    f"${(total_multi_daily / queries_per_day):,.4f}",
                    help="Average cost per query"
                )
            
            # Show savings analysis
            st.write("### 💰 Cost Analysis")
            analysis_cols = st.columns(3)
            
            with analysis_cols[0]:
                st.metric(
                    "Daily Savings",
                    f"${cost_difference:,.2f}",
                    f"{cost_difference_pct:.1f}%"
                )
            
            with analysis_cols[1]:
                st.metric(
                    "Annual Savings",
                    f"${cost_difference * 365:,.2f}",
                    help="Projected annual savings"
                )
            
            with analysis_cols[2]:
                st.metric(
                    "Savings per Query",
                    f"${cost_difference / queries_per_day:,.4f}",
                    help="Average savings per query"
                )
            
            # Add detailed breakdown
            with st.expander("📊 Detailed Cost Breakdown"):
                st.markdown(f"""
                ### Classification Overhead
                - Model: {classifier_model}
                - Daily cost: ${classifier_daily_cost['total_cost']:,.2f}
                - Cost per query: ${classifier_daily_cost['total_cost'] / queries_per_day:,.4f}
                """)
                
                for i, (model, percentage, cost) in enumerate(zip(models, percentages, model_costs)):
                    queries = int(queries_per_day * (percentage/100))
                    st.markdown(f"""
                    ### Model {i+1}: {model} ({percentage}% of queries)
                    - Queries handled: {queries:,}
                    - Full context cost: ${cost['input_cost']:,.2f}
                    - Processing cost: ${cost['output_cost']:,.2f}
                    - Total daily cost: ${cost['total_cost']:,.2f}
                    - Cost per query: ${cost['total_cost'] / queries:,.4f}
                    """)
        
        else:  # Compare Multi-Model Strategies
            strategy_1, strategy_2 = st.columns(2)
            
            # Strategy 1
            with strategy_1:
                st.write("### Strategy 1")
                classifier_1 = st.selectbox(
                    "Query Classification Model:",
                    df[cost_calculator.model_column].unique(),
                    key="strategy_1_classifier",
                    help="Model used to classify and route queries"
                )
                
                num_models_1 = st.number_input(
                    "Number of Models",
                    min_value=2,
                    max_value=5,
                    value=2,
                    key="strategy_1_models"
                )
                
                models_1 = []
                percentages_1 = []
                total_percentage_1 = 0
                model_costs_1 = []
                
                for i in range(num_models_1):
                    model = st.selectbox(
                        f"Model {i+1}:",
                        df[cost_calculator.model_column].unique(),
                        key=f"strategy_1_model_{i}"
                    )
                    models_1.append(model)
                    
                    if i == num_models_1 - 1:
                        percentage = 100 - total_percentage_1
                        st.write(f"Percentage: {percentage}%")
                    else:
                        percentage = st.slider(
                            f"Percentage for Model {i+1}",
                            0, 100-total_percentage_1,
                            value=min(50, 100-total_percentage_1),
                            key=f"strategy_1_percentage_{i}"
                        )
                    percentages_1.append(percentage)
                    total_percentage_1 += percentage
                    
                    # Calculate costs for each model
                    model_queries = int(queries_per_day * (percentage / 100))
                    model_cost = cost_calculator.calculate_cost(
                        model,
                        avg_input_tokens * queries_per_day,  # Full context for all queries
                        int(avg_input_tokens * avg_output_ratio) * model_queries  # Output only for this model's queries
                    )
                    model_costs_1.append(model_cost)
                
                # Calculate classification costs
                classifier_daily_cost_1 = cost_calculator.calculate_cost(
                    classifier_1,
                    100 * queries_per_day,  # Assuming 100 tokens per classification
                    50 * queries_per_day  # Assuming 50 tokens output for classification decision
                )
                
                # Calculate total strategy 1 costs
                total_strategy_1_daily = classifier_daily_cost_1['total_cost'] + sum(cost['total_cost'] for cost in model_costs_1)
                
                st.metric(
                    "Daily Cost",
                    f"${total_strategy_1_daily:,.2f}"
                )
                
                st.metric(
                    "Projected Annual Cost",
                    f"${(total_strategy_1_daily * 365):,.2f}",
                    help="Projected annual cost (365 days)"
                )
                
                st.metric(
                    "Cost per Query",
                    f"${(total_strategy_1_daily / queries_per_day):,.4f}",
                    help="Average cost per query"
                )
            
            # Strategy 2
            with strategy_2:
                st.write("### Strategy 2")
                classifier_2 = st.selectbox(
                    "Query Classification Model:",
                    df[cost_calculator.model_column].unique(),
                    key="strategy_2_classifier",
                    help="Model used to classify and route queries"
                )
                
                num_models_2 = st.number_input(
                    "Number of Models",
                    min_value=2,
                    max_value=5,
                    value=2,
                    key="strategy_2_models"
                )
                
                models_2 = []
                percentages_2 = []
                total_percentage_2 = 0
                model_costs_2 = []
                
                for i in range(num_models_2):
                    model = st.selectbox(
                        f"Model {i+1}:",
                        df[cost_calculator.model_column].unique(),
                        key=f"strategy_2_model_{i}"
                    )
                    models_2.append(model)
                    
                    if i == num_models_2 - 1:
                        percentage = 100 - total_percentage_2
                        st.write(f"Percentage: {percentage}%")
                    else:
                        percentage = st.slider(
                            f"Percentage for Model {i+1}",
                            0, 100-total_percentage_2,
                            value=min(50, 100-total_percentage_2),
                            key=f"strategy_2_percentage_{i}"
                        )
                    percentages_2.append(percentage)
                    total_percentage_2 += percentage
                    
                    # Calculate costs for each model
                    model_queries = int(queries_per_day * (percentage / 100))
                    model_cost = cost_calculator.calculate_cost(
                        model,
                        avg_input_tokens * queries_per_day,  # Full context for all queries
                        int(avg_input_tokens * avg_output_ratio) * model_queries  # Output only for this model's queries
                    )
                    model_costs_2.append(model_cost)
                
                # Calculate classification costs
                classifier_daily_cost_2 = cost_calculator.calculate_cost(
                    classifier_2,
                    100 * queries_per_day,  # Assuming 100 tokens per classification
                    50 * queries_per_day  # Assuming 50 tokens output for classification decision
                )
                
                # Calculate total strategy 2 costs
                total_strategy_2_daily = classifier_daily_cost_2['total_cost'] + sum(cost['total_cost'] for cost in model_costs_2)
                
                # Calculate cost difference for delta display
                cost_difference = total_strategy_1_daily - total_strategy_2_daily
                cost_difference_pct = (cost_difference / total_strategy_1_daily) * 100
                
                # Format delta string with appropriate sign
                if cost_difference >= 0:
                    delta_str = f"${abs(cost_difference):,.2f} ({abs(cost_difference_pct):.1f}%)"
                else:
                    delta_str = f"-${abs(cost_difference):,.2f} (-{abs(cost_difference_pct):.1f}%)"
                
                st.metric(
                    "Daily Cost",
                    f"${total_strategy_2_daily:,.2f}",
                    delta_str if cost_difference >= 0 else f"-{delta_str.lstrip('-')}",
                    delta_color="normal" if cost_difference >= 0 else "inverse"
                )
                
                st.metric(
                    "Projected Annual Cost",
                    f"${(total_strategy_2_daily * 365):,.2f}",
                    help="Projected annual cost (365 days)"
                )
                
                st.metric(
                    "Cost per Query",
                    f"${(total_strategy_2_daily / queries_per_day):,.4f}",
                    help="Average cost per query"
                )
            
            # Show savings analysis
            st.write("### 💰 Cost Analysis")
            analysis_cols = st.columns(3)
            
            with analysis_cols[0]:
                st.metric(
                    "Daily Savings",
                    f"${abs(cost_difference):,.2f}",
                    f"{abs(cost_difference_pct):.1f}%"
                )
            
            with analysis_cols[1]:
                st.metric(
                    "Annual Savings",
                    f"${abs(cost_difference * 365):,.2f}",
                    help="Projected annual savings"
                )
            
            with analysis_cols[2]:
                st.metric(
                    "Savings per Query",
                    f"${abs(cost_difference / queries_per_day):,.4f}",
                    help="Average savings per query"
                )
            
            # Add detailed breakdown
            with st.expander("📊 Detailed Cost Breakdown"):
                # Strategy 1 breakdown
                st.markdown("## Strategy 1")
                st.markdown(f"""
                ### Classification Overhead
                - Model: {classifier_1}
                - Daily cost: ${classifier_daily_cost_1['total_cost']:,.2f}
                - Cost per query: ${classifier_daily_cost_1['total_cost'] / queries_per_day:,.4f}
                """)
                
                for i, (model, percentage, cost) in enumerate(zip(models_1, percentages_1, model_costs_1)):
                    queries = int(queries_per_day * (percentage/100))
                    st.markdown(f"""
                    ### Model {i+1}: {model} ({percentage}% of queries)
                    - Queries handled: {queries:,}
                    - Full context cost: ${cost['input_cost']:,.2f}
                    - Processing cost: ${cost['output_cost']:,.2f}
                    - Total daily cost: ${cost['total_cost']:,.2f}
                    - Cost per query: ${cost['total_cost'] / queries:,.4f}
                    """)
                
                # Strategy 2 breakdown
                st.markdown("## Strategy 2")
                st.markdown(f"""
                ### Classification Overhead
                - Model: {classifier_2}
                - Daily cost: ${classifier_daily_cost_2['total_cost']:,.2f}
                - Cost per query: ${classifier_daily_cost_2['total_cost'] / queries_per_day:,.4f}
                """)
                
                for i, (model, percentage, cost) in enumerate(zip(models_2, percentages_2, model_costs_2)):
                    queries = int(queries_per_day * (percentage/100))
                    st.markdown(f"""
                    ### Model {i+1}: {model} ({percentage}% of queries)
                    - Queries handled: {queries:,}
                    - Full context cost: ${cost['input_cost']:,.2f}
                    - Processing cost: ${cost['output_cost']:,.2f}
                    - Total daily cost: ${cost['total_cost']:,.2f}
                    - Cost per query: ${cost['total_cost'] / queries:,.4f}
                    """)
    
    elif analysis_type == "Cost Visualization":
        st.subheader("Cost Visualization")
        # Add your original visualization options here
        
    # Token guide expander (available in all modes)
    with st.expander("ℹ️ How are tokens calculated?"):
        st.markdown("""
        📝 **Token Estimation Guide:**
        - Short words (1-2 chars): ~0.5 tokens
        - Average words (3-4 chars): ~1 token
        - Longer words: ~1 token per 4 characters
        - Numbers and punctuation are usually more efficient
        - Actual tokens may vary by model
        """)

except Exception as e:
    st.error(f"Error: {str(e)}") 