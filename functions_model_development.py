import re
import os
import io
import time
import itertools
import random
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_extras.stylable_container import stylable_container

from functions_admin import ChangeButtonColour

def delphi_questionnaire_inner_loop(vars_df, team, timestamp, var_type):
    st.session_state['cat_sub'] = vars_df.drop_duplicates(subset=['Category', 'Sub-category'])[['Category', 'Sub-category']].reset_index(drop = True)

    st.session_state['cat_sub_list'] = []
    for i in range(0, len(st.session_state['cat_sub'])):
        if st.session_state['cat_sub']['Category'][i] == st.session_state['cat_sub']['Sub-category'][i]:
            st.session_state['cat_sub_list'].append(st.session_state['cat_sub']['Category'][i])
        else:
            st.session_state['cat_sub_list'].append(str(st.session_state['cat_sub']['Category'][i] + " - " + st.session_state['cat_sub']['Sub-category'][i]))
    
    # Custom CSS for multiple headings with different background colors
    css_styles = """
    <style>
    """
    color_classes = ['#40597d', '#5e85b3', '#429bab', '#335e80', '#5f7c8f', '#41779c', '#3b7275', '#45567a', '#557e91']
    
    # Dynamically create CSS classes based on the number of items
    for i in range(len(st.session_state['cat_sub_list'])):
        css_styles += f"""
        .heading-{i+1} {{
            font-size: 24px;
            background-color: {color_classes[i % len(color_classes)]};
            color: white;
            padding: 10px;
            text-align: left;
            border-radius: 5px;
            # cursor: pointer;
            margin-bottom: 5px;
        }}
        """
    
    css_styles += """ 
    </style>
    """
    
    st.markdown(css_styles, unsafe_allow_html=True)

    for i, header in enumerate(st.session_state['cat_sub_list']):
        st.markdown(f'<div class="custom-header {f"heading-{i+1}"}">{header}</div>', unsafe_allow_html=True)

        temp_cat = st.session_state['cat_sub'][i:i+1]['Category'].reset_index(drop = True)[0]
        temp_sub = st.session_state['cat_sub'][i:i+1]['Sub-category'].reset_index(drop = True)[0]
        
        temp_df = vars_df[(vars_df['Category'] == temp_cat) & (vars_df['Sub-category'] == temp_sub)].reset_index(drop = True)

        # Custom CSS for better alignment
        st.markdown(
            """
            <style>
            .variable-row {
                display: flex;
                align-items: flex-start;
            }
            .blank-space {
                width: 100%;
                padding-right: 10px;
                font-weight: bold;
            }
            .variable-name {
                width: 100%;
                padding-right: 10px;
                font-weight: bold;
            }
            .variable-description {
                width: 100%;
                word-break: break-word;  /* Ensures long words break properly */
            }
            ol {
                padding-left: 20px;  /* Adjusts the padding for bullet points */
            }
            .variable-dropdown {
                width: 95%;
            }
            .high { color: green; }
            .medium { color: orange; }
            .low { color: red; }
            .divider {
                width: 100%;
                height: 0.1px;
                background-color: #E5D7D7; 
                margin: 2px;
            }
            </style>
            </style>
            """,
            unsafe_allow_html=True
        )

        # Display the variables with custom styling
        for i in range(len(temp_df)):
            
            var_name = temp_df['Variable Name'][i]
            description = convert_to_ordered_list(temp_df['Variable Description'][i])
            
            if f"{var_type}relevance_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}" not in st.session_state:
                st.session_state[f"{var_type}relevance_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"] = None

            if f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}" not in st.session_state:
                st.session_state[f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"] = None
            
            col1, col2, col3, col4, col5, col6 = st.columns([0.25, 4, 13, 5, 10, 0.25])
            with col2:
                st.markdown(f"""
                    <div class="variable-name">{temp_df['Variable Name'][i]}</div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="variable-description">{description}</div>
                """, unsafe_allow_html=True)
            with col4:
                options = ["High", "Medium", "Low"]
                
                if (st.session_state[f"{var_type}relevance_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"] != None):
                    # MAKE THE CHANGE HEREEEEEE
                    ind_val = options.index(st.session_state[f"{var_type}relevance_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"])
                else:
                    # ind_val = None
                    ind_val = random.choice([0,1,2])
                
                relevance = render_colored_dropdown(f"{var_type}relevance_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}", ind_val, options)
            with col5:
                st.markdown("""
                <style>
                .stTextArea label {
                    display: none;
                }
                </style>
                """, unsafe_allow_html=True)

                if st.session_state[f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"] != None:
                    val = st.session_state[f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"]
                else:
                    val = ''
                
                st.session_state[f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}"] = st.text_area(label="", value=val, placeholder=f"Comments for {temp_df['Variable Name'][i]}", key=f"{var_type}comment_{team, temp_cat, temp_sub, var_name, timestamp, st.session_state.user_name}_2")

            if i != len(temp_df)-1:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.session_state[f'{var_type}{team} delphi response'] = pd.DataFrame(columns = ['Model ID', 'Team', 'Category', 'Sub-category', 'Variable Name', 'Relevance', 'Comment'])
    
    for i in range(0, len(vars_df)):
        cat = vars_df['Category'][i]
        sub_cat = vars_df['Sub-category'][i]
        var = vars_df['Variable Name'][i]

        temp_df = pd.DataFrame([timestamp, team, cat, sub_cat, var, st.session_state[f"{var_type}relevance_{team, cat, sub_cat, var, timestamp, st.session_state.user_name}"], st.session_state[f"{var_type}comment_{team, cat, sub_cat, var, timestamp, st.session_state.user_name}"]]).T
        temp_df.columns = st.session_state[f'{var_type}{team} delphi response'].columns
        st.session_state[f'{var_type}{team} delphi response'] = pd.concat([st.session_state[f'{var_type}{team} delphi response'], temp_df]).reset_index(drop = True)

def convert_to_ordered_list(description):
    na_desc = False
    if pd.isna(description):
        na_desc = True
        description = "Description not available."

    # Split based on regex for numbers (1-9) followed by a dot and a space
    items = re.split(r'(?<=[2-9])\. ', description)
    ordered_list = '<ol>'
    for item in items:
        # Remove leading and trailing numbers and dots
        item = re.sub(r'^[0-9]+\.\s*', '', item)  # Remove leading numbers and dots
        item = re.sub(r'\s*[0-9]+$', '', item)  # Remove trailing numbers
        ordered_list += f'<li>{item.strip()}</li>'
    
    if na_desc == True:
        ordered_list = ordered_list[4:]
    else:
        ordered_list += '</ol>'

    return ordered_list


def render_colored_dropdown(key, ind_val, options):
    st.markdown("""
        <style>
        .stSelectbox {
            margin-top: -27px;  /* Adjust the negative margin as needed */
        }
        </style>
        """, unsafe_allow_html=True)
    # selected_option = st.selectbox("", options,
    #                                # MAKE CHANGES HERE
    #                                index=None, 
    #                                # index = random.choice([0,1,2]),
    #                                placeholder="Select relevance", key=key)

    st.session_state[key] = st.selectbox("", placeholder='Select Relevance', options=options, index = ind_val, key=f"{key}_2")

    return st.session_state[key]


def delphi_questionnaire_p1(team, product, timestamp):
    
    st.session_state['raw_vars_list'] = pd.read_excel('Variables.xlsx')

    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 95%;
            padding-left: 1%;
            padding-right: 1%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="big-font">Delphi Questionnaire for {team} Team - (1/2)</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Product: {product}</p>', unsafe_allow_html=True)
    
    
    vars_df = st.session_state['raw_vars_list'][st.session_state['raw_vars_list']['Page'] == 1].reset_index(drop = True)

    var_type = 'av_'
    delphi_questionnaire_inner_loop(vars_df, team, timestamp, var_type)
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 162px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    .divider {
                width = 70%;
                height: 0.1px;
                background-color: #E5D7D7; 
                margin: 2px;
            }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Initialize session state for handling page content display
    if f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}' not in st.session_state:
        st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] = False

    # Layout to center elements
    # col1, col2, col3 = st.columns(3)

    null_keys = [key for key in st.session_state if key.startswith(f'{var_type}relevance_') and st.session_state[key] is None]
 
    # with col2:  
    if (len(null_keys) != 0) & (st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] == False):
        col1, col2, col3 = st.columns(3)
        with col2: 
            st.markdown("""
                        <div style='text-align: center; 
                        background-color: #FFE7E7; 
                        color: #6E0202; 
                        padding-top: 15px; 
                        padding-bottom: 1px; 
                        border-radius: 5px;'>
                        <p>Select relevance for all fields.</p>
                        </div>
                        """, unsafe_allow_html=True)
            
    elif not st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}']:
        st.session_state.need_rerun = True


        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='b1'):
            st.session_state.page = 'pending_page_user'
            st.session_state.need_rerun = True
            if st.session_state.need_rerun:
                st.session_state.need_rerun = False
                st.rerun()
            
        
        ChangeButtonColour('Next', 'black', '#b3c3d9', '20px')
        if cols_button[3].button('Next', key='b2'):

            st.session_state['page'] = 'delphi_p2'
            st.session_state.need_rerun = True
            if st.session_state.need_rerun:
                st.session_state.need_rerun = False
                st.rerun()




                    

def delphi_questionnaire_p2(team, product, timestamp):
        
    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 95%;
            padding-left: 1%;
            padding-right: 1%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="big-font">Delphi Questionnaire for {team} Team - (2/2)</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Product: {product}</p>', unsafe_allow_html=True)
    
    vars_df = st.session_state['raw_vars_list'][st.session_state['raw_vars_list']['Page'] == 2].reset_index(drop = True)
    
    var_type = 'bv_'
    delphi_questionnaire_inner_loop(vars_df, team, timestamp, var_type)
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 162px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    .divider {
                width = 70%;
                height: 0.1px;
                background-color: #E5D7D7; 
                margin: 2px;
            }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 250px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'submit_delphi_ver_exp_run' not in st.session_state:
        st.session_state['submit_delphi_ver_exp_run'] = 0
    
    if f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}' not in st.session_state:
        st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] = False
    
    null_keys = [key for key in st.session_state if key.startswith(f'{var_type}relevance_') and st.session_state[key] is None]
    col1, col2, col3 = st.columns(3)
    with col2:  
        if (len(null_keys) != 0) & (st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] == False):
            st.markdown("""
                        <div style='text-align: center; 
                        background-color: #FFE7E7; 
                        color: #6E0202; 
                        padding-top: 15px; 
                        padding-bottom: 1px; 
                        border-radius: 5px;'>
                        <p>Select relevance for all fields.</p>
                        </div>
                        """, unsafe_allow_html=True)
    if (st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] == False) & (len(null_keys) == 0):
        cols = st.columns(6)
        with cols[2]:

            cols_button = st.columns(1)
            ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
            if cols_button[0].button('Back', key='back_delphi_p2'):
            
            # if st.button('Back'):
                st.session_state['page'] = 'delphi_p1'
                st.session_state['submit_delphi_ver'] = False
                st.session_state.need_rerun = True
                st.session_state.need_rerun = False
                st.rerun()
    
        with cols[3]:


            st.markdown("""
            <style>
            .stPopoverBody {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding-bottom: 0px;
            width: 100%;
            }
            p, ol, ul, dl {
                font-size: 14px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with stylable_container(
                key="deploy_popover",
                css_styles="""
                    button {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-top: -7px;
                        width: 100%;
                        color: black;
                        font-size: 14px;
                        # text-decoration: underline;
                        background-color: #b3c3d9;
                        border-radius: 50px;
                    }
                    """,
            ):
            
                with st.popover("Submit Response"):
                    st.markdown(f"<div class='stPopoverBody'>Are you sure you want to submit?</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='stPopoverBody'>Changes can not be made later.</div>", unsafe_allow_html=True)

                    cols_button = st.columns([1, 2, 1])
                    ChangeButtonColour('Yes', 'black', '#b3c3d9', '20px', margin_bottom = '-40px')
                    if cols_button[1].button('Yes', key='submit_delphi_p2'):
                        st.session_state[f'{var_type}submitted_{team}_ahp_{timestamp}{st.session_state.user_name}'] = True
                        
                        st.session_state[f'{team} delphi response'] = pd.concat([st.session_state[f'av_{team} delphi response'], st.session_state[f'bv_{team} delphi response']]).reset_index(drop=True)
        
                        st.session_state[f'{team} delphi response'].insert(2, 'User', st.session_state.email)
                        st.session_state[f'{team} delphi response'].insert(1, 'Product', product)
                        st.session_state[f'{team} delphi response'].insert(0, 'Added At', datetime.now())
                        
                        response_excel = pd.read_excel('Response.xlsx')
                        response_excel = pd.concat([response_excel, st.session_state[f'{team} delphi response']], ignore_index=True)
                        response_excel.to_excel('Response.xlsx', index=False)
        
                        assigned_forms = pd.read_excel('assign_forms.xlsx')
                        
                        assigned_forms.loc[((assigned_forms['model_id'] == timestamp) & 
                                            (assigned_forms['product'] == product) & 
                                            (assigned_forms['team'] == team) & 
                                            (assigned_forms['user'] == st.session_state.email) & 
                                            (assigned_forms['questionnaire'] == 'Delphi')), 'completed'] = 1
                
                        assigned_forms.loc[((assigned_forms['model_id'] == timestamp) & 
                                            (assigned_forms['product'] == product) & 
                                            (assigned_forms['team'] == team) & 
                                            (assigned_forms['user'] == st.session_state.email) & 
                                            (assigned_forms['questionnaire'] == 'Delphi')), 'reviewed'] = 1
                
                        assigned_forms.loc[((assigned_forms['model_id'] == timestamp) & 
                                            (assigned_forms['product'] == product) & 
                                            (assigned_forms['team'] == team) & 
                                            (assigned_forms['user'] == st.session_state.email) & 
                                            (assigned_forms['questionnaire'] == 'Delphi') & 
                                            (assigned_forms['reviewer'] == 'Yes')), 'reviewed'] = 0
                
                        # assigned_forms.to_excel('assign_forms.xlsx', index=False)
                        with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            assigned_forms.to_excel(writer, sheet_name='Sheet1', index=False)
        
                        st.session_state['page'] = 'pending_page_user'
            
                        st.session_state.need_rerun = True
                        if st.session_state.need_rerun:
                            st.session_state.need_rerun = False
                            st.rerun()





def display_table(df, header, header_background_color):
       
    # CSS to center the elements, remove padding, and align checkbox to the right
    st.markdown("""
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        hr {
            margin-top: 0px;
            margin-bottom: 0px;
            background-color: #9c9b99; 
        }
        .boldhr {
            width: 100%;
            height: 2px;
            background-color: #9c9b99; 
            # margin: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
    .heading-{header_background_color}{{
            font-size: 20px;
            background-color: #{header_background_color};
            color: white;
            padding: 5px;
            text-align: left;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 5px;  # Corrected to a single margin-bottom property
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="heading-{header_background_color}">{header}</div>', unsafe_allow_html=True) 
    
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)  # Divider
    
    cols = st.columns([0.45, 0.45, 0.45, 0.13, 0.13, 0.13, 0.3, 0.08, 0.6, 0.6, 0.6])
    
    header_labels = [
        'Category', 'Sub-category', 'Variable Name', 'High', 'Medium', 'Low', 'Relevance', 'Selected', 'Reason', 'Comments from Responses', 'Your Comments'] 
    
    st.session_state[f'{header} delphi response verification'] = pd.DataFrame(columns = ['Model ID'] + header_labels)
    
    for i, label in enumerate(header_labels):
        with cols[i]:
            st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 10px'>{label}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    for i, row in df.iterrows():
        row_color = '#FFFFFF'
        cols = st.columns([0.45, 0.45, 0.45, 0.13, 0.13, 0.13, 0.3, 0.08, 0.6, 0.6, 0.6])
    
        if f"deplhi_ver_toggle_{i}" not in st.session_state:
            st.session_state[f"deplhi_ver_toggle_{i}"] = None
        
        if f"delphi_ver_comment_{i}" not in st.session_state:
            st.session_state[f"delphi_ver_comment_{i}"] = None
        
        temp_df_list = [st.session_state.delphi_ver_model]
        
        for j, column in enumerate(cols):
            with column:
                if j < 7:  # For all columns except checkbox and text input
                    if j == 6:
                        if row[df.columns[j+6]] == 'High': back_color, font_color = '#cff7cf', 'Green'
                        if row[df.columns[j+6]] == 'Medium': back_color, font_color = '#fcf8e2', '#a2ab00'
                        if row[df.columns[j+6]] == 'Low': back_color, font_color = '#f7cfcf', 'Red'
                        st.markdown(f"<div class='centered' style='padding: 4px; color: {font_color}; background-color: {back_color}; font-weight: bold; margin: auto; width: 70%'>{row[df.columns[j+6]]}</div>", unsafe_allow_html=True)
    
                        temp_df_list.append(row[df.columns[j+6]])
                    
                    else:
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;'>{row[df.columns[j]]}</div>", unsafe_allow_html=True)
                        temp_df_list.append(row[df.columns[j]])
                        
                elif j == 7:  # For checkbox
                    
                    if row['Relevance'] in ['High', 'Medium']:
                        ind_option = True
                    else:
                        ind_option = False
    
                    if (st.session_state[f"deplhi_ver_toggle_{i}"] != ind_option) & (st.session_state[f"deplhi_ver_toggle_{i}"] != None):
                        ind_option = st.session_state[f"deplhi_ver_toggle_{i}"]
                        
                    st.session_state[f"deplhi_ver_toggle_{i}"] = st.checkbox("",value = ind_option, key=f"deplhi_ver_toggle_{i}_2")
                    temp_df_list.append(st.session_state[f"deplhi_ver_toggle_{i}"])
                        
                elif j == 8:
                    if row ['Relevance'] == 'High':
                        reason = "Included on unanimity."
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;'>{reason}</div>", unsafe_allow_html=True)
                        temp_df_list.append(reason)
                    elif row ['Relevance'] == 'Low':
                        reason = "Excluded on unanimity."
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;'>{reason}</div>", unsafe_allow_html=True)
                        temp_df_list.append(reason)
                    elif row ['Relevance'] == 'Medium':
                        reason = "Retained for balanced assessment."
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;'>{reason}</div>", unsafe_allow_html=True)
                        temp_df_list.append(reason)
    
                
                
                elif j == 9:
                    if row['Combined Comments'] == ' ':
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;'>N/A</div>", unsafe_allow_html=True)
                        temp_df_list.append('N/A')
                    else: #re.sub(r'(\w+:)', r"<span style='font-weight:bold;'>\1</span>", row['Combined Comments'])
                        # formatted_text = re.sub(r'^(.+?:)', r"<b>\1</b>", row['Combined Comments'], flags=re.M)
                        temp_df_list.append(row['Combined Comments'])
                        
                        # # Display the formatted text with HTML enabled
                        # st.write(formatted_text, unsafe_allow_html=True)
                        # # st.write(f"{row['Combined Comments']}\n\n")

                        formatted_text = modified_text = re.sub(
                            r'^(.+?:)\s*(.*)$',
                            r"<span style='font-size: 16px; font-weight: bold;'>\1</span> <span style='font-size: 16px; line-height: 1;'>\2</span>",
                            row['Combined Comments'], flags=re.M)
                        
                        st.markdown(f"<div style='line-height: 1; margin-top: 5px;'>{formatted_text}</div>", unsafe_allow_html=True)
                        
                elif j == 10:  # For text input
                    if (st.session_state[f"delphi_ver_comment_{i}"] != ''):
                        text_val = st.session_state[f"delphi_ver_comment_{i}"]
                    else:
                        text_val = ''
                        
                    st.session_state[f"delphi_ver_comment_{i}"] = st.text_input("", value = text_val, key=f"delphi_ver_comment_{i}_2", placeholder = "Enter comment", label_visibility="collapsed")
                    temp_df_list.append(st.session_state[f"delphi_ver_comment_{i}"])
    
                    # else:
                    #     st.session_state[f"delphi_ver_comment_{i}"] = st.text_input("", value = st.session_state[f"delphi_ver_comment_{i}"], key=f"delphi_ver_comment_{i}_2", placeholder="Enter comment", label_visibility="collapsed")
                        
                    #     temp_df_list.append(st.session_state[f"delphi_ver_comment_{i}"])
        
        st.markdown("<hr>", unsafe_allow_html=True)
    
        temp_df = pd.DataFrame(temp_df_list).T
        temp_df.columns = st.session_state[f'{header} delphi response verification'].columns
        st.session_state[f'{header} delphi response verification'] = pd.concat([st.session_state[f'{header} delphi response verification'], temp_df]).reset_index(drop = True)



def combine_comments(group):
    return ' \n\n'.join(group['Labeled Comments'])

    
def delphi_verification_form():

    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 95%;
        padding-left: 1%;
        padding-right: 1%;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="big-font">Delphi Questionnaire Verification</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Product: {st.session_state['product']}</p>', unsafe_allow_html=True)
    
    merged = pd.read_excel('Response.xlsx')
    merged = merged[merged['Model ID'] == st.session_state.delphi_ver_model].reset_index(drop = True)

    summarized = merged.groupby(['Category', 'Sub-category', 'Variable Name'])['Relevance'].value_counts().unstack(fill_value=0)
    summarized = summarized.merge(merged.groupby(['Category', 'Sub-category', 'Variable Name']).agg(Count = ('Variable Name', 'count')),
                                  how = 'left', on = ['Category', 'Sub-category', 'Variable Name']).reset_index()

    if 'Low' in summarized.columns:
        col_low = summarized.pop('Low')
        summarized.insert(summarized.columns.get_loc('Medium') + 1, 'Low', col_low)
    
    # Sort and create labeled comments
    merged['Comment'] = merged['Comment'].fillna('')
    comm_merger = merged.loc[merged['Comment'] != '']
    comm_merger['Comment'] = comm_merger['Comment'].astype(str)

    users = pd.read_excel('Users.xlsx')

    comm_merger = comm_merger.merge(users[['email', 'f_name', 'l_name']], how = 'left', left_on = 'User', right_on = 'email').drop('email', axis = 1)
    
    comm_merger['Labeled Comments'] = comm_merger['f_name'].fillna('') + ' ' + comm_merger['l_name'].fillna('') + ' (' + comm_merger['Team'] + '): ' + comm_merger['Comment'].str.lstrip()
    
    # st.write(comm_merger)

    
    if len(comm_merger) > 0:
        combined_comments = comm_merger.groupby(['Category', 'Sub-category', 'Variable Name']).apply(combine_comments).reset_index(name='Combined Comments')
    else:
        combined_comments = pd.DataFrame(columns = ['Category', 'Sub-category', 'Variable Name', 'Combined Comments'])
    
    summarized = summarized.merge(combined_comments, how = 'left', on = ['Category', 'Sub-category', 'Variable Name'])
    summarized['Combined Comments'] = summarized['Combined Comments'].fillna(' ')
    
    if 'High' not in summarized.columns: 
        summarized['High'] = 0
    if 'Medium' not in summarized.columns: 
        summarized['Medium'] = 0
    if 'Low' not in summarized.columns: 
        summarized['Low'] = 0
    
    summarized['Relevance Value'] = (5*summarized['High']/6 + 1*summarized['Medium']/2 + 1*summarized['Low']/6)/summarized['Count']
    summarized['High ther'] = 2/3
    summarized['Med ther'] = 1/2
    summarized['Low ther'] = 1/3
    
    summarized['Relevance'] = 'Low'
    summarized.loc[(summarized['Relevance Value']>summarized['Low ther']) & (summarized['Relevance Value']<summarized['High ther']), 'Relevance'] = 'Medium'
    summarized.loc[(summarized['Relevance Value']>=summarized['High ther']), 'Relevance'] = 'High'
    # st.write(summarized)
    
    # Display Application Variables
    display_table(summarized[~summarized['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])], 'Application Variables', '335e80')
    # Display Behavioral Variables
    display_table(summarized[summarized['Category'] == 'Behavioral Variables'], 'Behavioral Variables', '5e85b3')
    # Display 'Adjustments / Downgrade Factors
    display_table(summarized[summarized['Category'] == 'Adjustments / Downgrade Factors'], 'Adjustments / Downgrade Factors', '326aab')
    # Display Early Warning Indicators
    display_table(summarized[summarized['Category'] == 'Early Warning Indicators'], 'Early Warning Indicators', '5393db')

    st.session_state['delphi response verification'] = pd.concat([st.session_state[f'{'Application Variables'} delphi response verification'], st.session_state[f'{'Behavioral Variables'} delphi response verification'], st.session_state[f'{'Adjustments / Downgrade Factors'} delphi response verification'], st.session_state[f'{'Early Warning Indicators'} delphi response verification']]).reset_index(drop = True)
    
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 250px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    </style>
    """, unsafe_allow_html=True)

    # st.write(st.session_state['delphi response verification'])

    errors_list = []

    if len(st.session_state['delphi response verification'].loc[(st.session_state['delphi response verification']['Selected'] == True) & (~st.session_state['delphi response verification']['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators']))]) == 0:
        errors_list.append('At-least one variable should be selected from Application Variables.')

    if len(st.session_state['delphi response verification'].loc[(st.session_state['delphi response verification']['Selected'] == True) & (st.session_state['delphi response verification']['Category'].isin(['Behavioral Variables']))]) == 0:
        errors_list.append('At-least one variable should be selected from Behavioral Variables.')

    if len(st.session_state['delphi response verification'].loc[(st.session_state['delphi response verification']['Selected'] == True) & (st.session_state['delphi response verification']['Category'].isin(['Adjustments / Downgrade Factors']))]) == 0:
        errors_list.append('At-least one variable should be selected from Adjustments / Downgrade Factors.')

    if len(st.session_state['delphi response verification'].loc[(st.session_state['delphi response verification']['Selected'] == True) & (st.session_state['delphi response verification']['Category'].isin(['Early Warning Indicators']))]) == 0:
        errors_list.append('At-least one variable should be selected from Early Warning Indicators.')
        
    if len(errors_list) > 0:
        cols = st.columns([2, 3, 2])
        with cols[1]:
            markdown_text = "<ul>" + "".join([f"<li>{text}</li>" for text in errors_list]) + "</ul>"
        
            st.markdown(f"""<div style='text-align: left; background-color: #FFE7E7; color: #6E0202; padding-top: 15px; padding-bottom: 1px; padding-left: 4px; border-radius: 5px;'>{markdown_text}</div>""", unsafe_allow_html=True)
   
    else:
        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='main_page_back_ver_list'):
            st.session_state.page = 'pending_page_user'
            st.session_state.need_rerun = True
            if st.session_state.need_rerun:
                st.session_state.need_rerun = False
                st.rerun()

        
        ChangeButtonColour('View Shortlisted Variables', 'black', '#b3c3d9', '20px')
        if cols_button[3].button('View Shortlisted Variables', key=f'shrt_list_vars_{st.session_state.product}'):
            st.session_state['page'] = 'delphi_short_list_vars'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()


def delphi_shortlist_var():
    st.session_state['raw_vars_list'] = pd.read_excel('Variables.xlsx')

    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 95%;
        padding-left: 1%;
        padding-right: 1%;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    # img_title("EY Logo.png")
    
    # st.header(f'Delphi Questionnaire for Team {team}')
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="big-font">Shortlisted Variables Pre-AHP</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Product: {st.session_state.product}</p>', unsafe_allow_html=True)
    
    shortlisted_vars = st.session_state['delphi response verification'].loc[st.session_state['delphi response verification']['Selected'] == True][['Category', 'Sub-category', 'Variable Name']].reset_index(drop = True)
    
    shortlisted_vars = shortlisted_vars.merge(st.session_state['raw_vars_list'],
                                           how = 'left',
                                           on = ['Category', 'Sub-category', 'Variable Name'])

    # CSS to center the elements, remove padding, and align checkbox to the right
    st.markdown("""
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        hr {
            margin-top: 0px;
            margin-bottom: 0px;
            background-color: #9c9b99; 
        }
        .boldhr {
            width: 100%;
            height: 2px;
            background-color: #9c9b99; 
            # margin: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)  # Divider
    
    cols = st.columns([1, 1, 1, 6])
    
    header_labels = ['Category', 'Sub-category', 'Variable Name', 'Description']

    # display_shortlitsed_vars = pd.DataFrame(columns = header_labels)
    
    for i, label in enumerate(header_labels):
        with cols[i]:
            st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 10px'>{label}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    for i in range(0, len(shortlisted_vars)):
        if shortlisted_vars['Category'][i] != shortlisted_vars['Sub-category'][i]:
            cols = st.columns([1, 1, 1, 6])
            with cols[0]:
                # st.write()
                st.markdown(f"<div class='centered' style='margin-top: 10px'>{shortlisted_vars['Category'][i]}</div>", unsafe_allow_html=True)
            with cols[1]:
                # st.write()
                st.markdown(f"<div class='centered' style='margin-top: 10px'>{shortlisted_vars['Sub-category'][i]}</div>", unsafe_allow_html=True)
            with cols[2]:
                # st.write()
                st.markdown(f"<div class='centered' style='margin-top: 10px'>{shortlisted_vars['Variable Name'][i]}</div>", unsafe_allow_html=True)
            with cols[3]:
                st.write(shortlisted_vars['Variable Description'][i])

        else:
            cols = st.columns([2, 1, 6])
            with cols[0]:
                # st.write()
                st.markdown(f"<div class='centered' style='margin-top: 10px'>{shortlisted_vars['Category'][i]}</div>", unsafe_allow_html=True)
            with cols[1]:
                # st.write()
                st.markdown(f"<div class='centered' style='margin-top: 10px'>{shortlisted_vars['Variable Name'][i]}</div>", unsafe_allow_html=True)
            with cols[2]:
                description = shortlisted_vars['Variable Description'][i]
                st.write(description if pd.notna(description) else 'Description not available.')

        st.markdown("<hr>", unsafe_allow_html=True)


    if 'User' not in st.session_state['delphi response verification'].columns:
        st.session_state['delphi response verification'].insert(1, 'User', st.session_state.email)
    if 'Product' not in st.session_state['delphi response verification'].columns:
        st.session_state['delphi response verification'].insert(1, 'Product', st.session_state.product)
    if 'Added At' not in st.session_state['delphi response verification'].columns:
        st.session_state['delphi response verification'].insert(0, 'Added At', datetime.now())

    # st.write(st.session_state['delphi response verification'])

    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 250px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    </style>
    """, unsafe_allow_html=True)

    if f'submit_delphi_ver_{st.session_state.model_id}' not in st.session_state:
        st.session_state[f'submit_delphi_ver_{st.session_state.model_id}'] = False

    if 'submit_delphi_ver_exp_run' not in st.session_state:
        st.session_state['submit_delphi_ver_exp_run'] = 0

    if st.session_state[f'submit_delphi_ver_{st.session_state.model_id}'] == False:
        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='back_delphi_ver'):
            st.session_state['page'] = 'delphi_ver'
            st.session_state[f'submit_delphi_ver_{st.session_state.model_id}'] = False
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()






        st.markdown("""
        <style>
        .stPopoverBody {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding-bottom: 0px;
        width: 100%;
        }
        p, ol, ul, dl {
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)

        with cols_button[3]:
            with stylable_container(
                key="deploy_popover",
                css_styles="""
                    button {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-top: 10px;
                        width: 100%;
                        color: black;
                        font-size: 14px;
                        # text-decoration: underline;
                        background-color: #b3c3d9;
                        border-radius: 50px;
                    }
                    """,
            ):
            
                with st.popover("Submit Response"):
                    st.markdown(f"<div class='stPopoverBody'>Are you sure you want to submit?</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='stPopoverBody'>Changes can not be made later.</div>", unsafe_allow_html=True)

                    yes_cols = st.columns([1, 2, 1])
                    ChangeButtonColour('Yes', 'black', '#b3c3d9', '20px', margin_bottom = '-40px')
                    if yes_cols[1].button('Yes', key='submit_delphi_vars_short'):
                    # if st.button('Submit Response'):
                        st.session_state[f'submit_delphi_ver_{st.session_state.model_id}'] = True 
            
                        delphi_ver_excel = pd.read_excel('Delphi Verification Responses.xlsx')
                        delphi_ver_excel = pd.concat([delphi_ver_excel, st.session_state['delphi response verification']], ignore_index=True)
                        delphi_ver_excel.to_excel('Delphi Verification Responses.xlsx', index=False)
                    
                        # st.write(delphi_ver_excel)
                        assigned_forms = pd.read_excel('assign_forms.xlsx')
                        # st.write(assigned_forms,  st.session_state.model_id,  st.session_state.product,  st.session_state.email)
                        
                        assigned_forms.loc[((assigned_forms['model_id'] == st.session_state.model_id) & 
                                            (assigned_forms['product'] == st.session_state.product) & 
                                            (assigned_forms['user'] == st.session_state.email) & 
                                            (assigned_forms['questionnaire'] == 'Delphi')), 'reviewed'] = 1
            
                        with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            assigned_forms.to_excel(writer, sheet_name='Sheet1', index=False)
            
                        st.session_state['page'] = 'pending_page_user'
                        st.session_state.need_rerun = True
                        if st.session_state.need_rerun:
                            st.session_state.need_rerun = False
                            st.rerun()
                            

def ahp_questionnaire(team, model_id, shortlisted_vars):
    st.session_state.ahp_selection_df = pd.DataFrame(columns = ['Model ID', 'Product', 'User', 'Category', 'Sub-category', 'Criteria 1', 'Criteria 2', 'Selection', 'Magnitude'])
    
    cols = ['Model ID',	'Team',	'Level', 'Category', 'Sub-category', 'Variable Name', 'Weight']
    st.session_state[f'ahp_weights_{team}'] = pd.DataFrame(columns = cols)
        
    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 80%;
        padding-left: 1%;
        padding-right: 1%;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    # img_title("EY Logo.png")
    
    st.markdown("""
        <style>
        .big-font {
            font-size:25px !important;
            font-weight: bold;
            margin-top: -40px;
            padding: 0px;
        }
        .small-font {
            font-size:20px !important;
            # font-weight: bold;
            margin-bottom: 0px;
        }
        .boldhr {
            width: 100%;
            height: 2px;
            background-color: #9c9b99; 
            # margin: 2px;
            # margin-bottom: -5px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="big-font">AHP Questionnaire for {team}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font" style="margin-top:-30px;">Product: {st.session_state.product}</p>', unsafe_allow_html=True)

    # st.image('AHP Process.png')
    
    color_classes = ['#40597d', '#5e85b3', '#429bab', '#335e80', '#5f7c8f', '#41779c', '#3b7275', '#45567a', '#557e91']
    


    with st.expander('Application Variables'):
        variables = list(pd.unique(shortlisted_vars.loc[~shortlisted_vars['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])]['Category']))
        if len(variables) != 0:
            # st.markdown(f'<p class="small-font">Application Variables</p>', unsafe_allow_html=True)
            # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
            
            ahp_questionnaire_calcs('L2 - Customer Specific Categories', None, None, variables, '#04695b', 'cs', team, 'L2', model_id)
            st.write('\n')
            
            cat_count = 0
            for cat in pd.unique(variables):
                if list(pd.unique(shortlisted_vars[shortlisted_vars['Category'] == cat]['Sub-category'])) == [cat]:
                    temp_df = pd.DataFrame([model_id, team, 'L3', cat, cat, None, 1]).T
                    temp_df.columns = st.session_state[f'ahp_weights_{team}'].columns
                    st.session_state[f'ahp_weights_{team}'] = pd.concat([st.session_state[f'ahp_weights_{team}'], temp_df]).reset_index(drop = True)
                    
                    ahp_questionnaire_calcs(f"L3 - {cat}", cat, cat, pd.unique(shortlisted_vars[(shortlisted_vars['Category'] == cat)]['Variable Name']), color_classes[cat_count], cat_count, team, 'L4', model_id)
            
                else: 
                    ahp_questionnaire_calcs(f"L3 - {cat}", cat, None, pd.unique(shortlisted_vars[(shortlisted_vars['Category'] == cat)]['Sub-category']), color_classes[cat_count], cat_count, team, 'L3', model_id)
            
                    for sub_cat in pd.unique(shortlisted_vars[shortlisted_vars['Category'] == cat]['Sub-category']):
                        temp_vars = pd.unique(shortlisted_vars[(shortlisted_vars['Category'] == cat) & (shortlisted_vars['Sub-category'] == sub_cat)]['Variable Name']) 
                        ahp_questionnaire_calcs(f"L4 - {cat}: {sub_cat}", cat, sub_cat, temp_vars, color_classes[cat_count], cat_count, team, 'L4', model_id)
                
                st.write('\n')
                cat_count += 1



    with st.expander('Behavioral Variables'):
        # st.markdown(f'<p class="small-font">Behavioral Variables</p>', unsafe_allow_html=True)
        # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
        
        bv_vars = shortlisted_vars.loc[shortlisted_vars['Category'] == 'Behavioral Variables']['Variable Name']
        ahp_questionnaire_calcs('L4 - Variables', 'Behavioral Variables', 'Behavioral Variables', bv_vars, '#4354ab', 'bv', team, 'L4', model_id)
        st.write('\n')

    with st.expander('Adjustments / Downgrade Factors'):
        if len(shortlisted_vars.loc[shortlisted_vars['Category'] == 'Adjustments / Downgrade Factors']) != 0:
            # st.markdown(f'<p class="small-font">Adjustments / Downgrade Factors</p>', unsafe_allow_html=True)
            # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
            af_vars = shortlisted_vars.loc[shortlisted_vars['Category'] == 'Adjustments / Downgrade Factors']['Variable Name']
            ahp_questionnaire_calcs('L4 - Variables', 'Adjustments / Downgrade Factors', 'Adjustments / Downgrade Factors', af_vars, '#a9ab32', 'af', team, 'L4', model_id)
            st.write('\n')

    with st.expander('Early Warning Indicators'):
        if len(shortlisted_vars.loc[shortlisted_vars['Category'] == 'Early Warning Indicators']) != 0:
            # st.markdown(f'<p class="small-font">Early Warning Indicators</p>', unsafe_allow_html=True)
            # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
            ewi_vars = shortlisted_vars.loc[shortlisted_vars['Category'] == 'Early Warning Indicators']['Variable Name']
            ahp_questionnaire_calcs('L4 - Variables', 'Early Warning Indicators', 'Early Warning Indicators', ewi_vars, '#32ab7e', 'ewi', team, 'L4', model_id)
            st.write('\n')

    

    

    null_keys_consistency = [key for key in st.session_state if key.startswith('ahp_consistency_check_') and key.endswith(f'_{st.session_state.user_name}') and st.session_state[key] == False]
    null_keys_better_field = [key for key in st.session_state if key.startswith('ahp_better_dropdown_') and key.endswith(f"{st.session_state.user_name}')") and st.session_state[key] is None]
    null_keys_magnitude = [key for key in st.session_state if key.startswith('ahp_magnitude_dropdown_') and key.endswith(f"{st.session_state.user_name}')")  and st.session_state[key] is None]
    
    # st.write(null_keys_consistency)
    if (len(null_keys_magnitude) > 0) or (len(null_keys_better_field) > 0): # or (len(null_keys_consistency) > 0):
        cols = st.columns(3)
        with cols[1]:
            st.markdown("""<div style='text-align: center; background-color: #FFE7E7; color: #6E0202; padding-top: 15px; padding-bottom: 1px; border-radius: 5px;'><p>All fields should be populated.</p></div>""", unsafe_allow_html=True)

            st.write('')
            
        cols_button = st.columns([1, 0.8, 1])
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        
        if cols_button[1].button('Back', key='ahp_back_home'):
            st.session_state['page'] = 'ahp_questionnaire_description'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()
        
    elif len(null_keys_consistency) > 0:
        cols = st.columns(3)
        with cols[1]:
            st.markdown("""<div style='text-align: center; background-color: #FFE7E7; color: #6E0202; padding-top: 15px; padding-bottom: 1px; border-radius: 5px;'><p>All the responses must be consistent.</p></div>""", unsafe_allow_html=True)

            st.write('')

        cols_button = st.columns([1, 0.8, 1])
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        
        if cols_button[1].button('Back', key='ahp_back_home'):
            st.session_state['page'] = 'ahp_questionnaire_description'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()

    else:
        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='ahp_back_home'):
            st.session_state['page'] = 'pending_page_user'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()
        
        ChangeButtonColour('Verify Weights', 'black', '#b3c3d9', '20px')
        if cols_button[3].button('Verify Weights', key='verify_weights'):
            st.session_state['page'] = 'ahp_questionnaire_weights'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()


def ahp_questionnaire_calcs(header, cat, sub_cat, variables, header_background_color, cat_count, team, level, model_id):
    # st.write(header_background_color)
    header_background_color = '#5e85b3'

    if f"ahp_consistency_check_{team}_{variables}_{model_id}_{st.session_state.user_name}" not in st.session_state:
        st.session_state[f"ahp_consistency_check_{team}_{variables}_{model_id}_{st.session_state.user_name}"] = False
    
    st.markdown(f"""
    <style>
    .heading-{cat_count}{{
            font-size: 15px;
            background-color: {header_background_color};
            color: white;
            padding-left: 5px;
            text-align: left;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 0px;  # Corrected to a single margin-bottom property
            # margin-top: 10px; 
    }}
    .centered {{
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 20px;  # Uncommented and assumed you want it active
    }}
    hr {{
        margin-top: 0px;
        margin-bottom: -5px;
        background-color: #9c9b99; 
    }}
    .boldhr {{
        margin-top: -5px;
        margin-bottom: -5px;
        width: 100%;
        height: 2px;
        background-color: #9c9b99;
        margin: 2px;  # Uncommented and assumed you want it active
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="heading-{cat_count}">{header}</div>', unsafe_allow_html=True)
    
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)

    if len(variables) == 1:
        temp_variables = list(variables)
        st.markdown(f"<div style='font-size: 15px;'>100% weight assigned to <strong>{temp_variables[0]}</strong> because it was the only variable shortlisted for this classification.</div>", unsafe_allow_html=True)
        
        if level == 'L2':
            temp_df = pd.DataFrame([model_id, team, level, temp_variables[0], None, None, 1]).T

        elif level == 'L3':
            temp_df = pd.DataFrame([model_id, team, level, cat, temp_variables[0], None, 1]).T

        elif level == 'L4':
            temp_df = pd.DataFrame([model_id, team, level, cat, sub_cat, temp_variables[0], 1]).T
            
        temp_df.columns = st.session_state[f'ahp_weights_{team}'].columns
        st.session_state[f'ahp_weights_{team}'] = pd.concat([st.session_state[f'ahp_weights_{team}'], temp_df]).reset_index(drop = True)
        st.session_state[f"ahp_consistency_check_{team}_{variables}_{model_id}_{st.session_state.user_name}"] = True
        
    else:
        cols = st.columns([1,1,1,0.2,1])
        
        header_labels = ['Criteria 1', 'Criteria 2', 'Which is better?', '', 'Magnitude (1-10)']
        for i, label in enumerate(header_labels):
            with cols[i]:
                st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: -10px; font-size: 15px;'>{label}</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        combinations = list(itertools.combinations(variables, 2))
        
        columns = variables
        index = variables
        
        matrix = pd.DataFrame(index=index, columns=columns)
        for var in variables:
            matrix[var][var] = 1
        
        for i in range(0, len(combinations)):

            criteria_df_list = [st.session_state.model_id, st.session_state.product, st.session_state.email, cat if cat is not None else 'NA', header if header is not None else 'NA', combinations[i][0], combinations[i][1]]
    
            if f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}" not in st.session_state:
                st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] = None
            
            if f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}" not in st.session_state:
                st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] = None
            
            cols = st.columns([1,1,1,0.2,1])
            
            for j, column in enumerate(cols):
                
                with column:
                    if j == 0:
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto; font-size: 15px;'>{combinations[i][0]}</div>", unsafe_allow_html=True)
            
                    elif j == 1:
                        st.markdown(f"<div class='centered' style='padding: 4px; margin: auto;  font-size: 15px;'>{combinations[i][1]}</div>", unsafe_allow_html=True)
    
                    elif j == 2:
                        st.markdown("""
                        <style>
                        .stSelectbox {
                            margin-top: -45px;
                            width: 50%;
                        }
                        </style>
                        """, unsafe_allow_html=True)

                        if (st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] != None):
                            ind_val = [combinations[i][0], combinations[i][1]].index(st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"])
                        else:
                            ind_val = None
                            
                        st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] = st.selectbox("", placeholder='Select Variable', options=[combinations[i][0], combinations[i][1]], index = ind_val, key=f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}_2")

                        criteria_df_list.append(st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"])
                    
                    elif j == 4:
                        st.markdown("""
                        <style>
                        .stSelectbox {
                            margin-top: -45px;
                            width: 50%;
                        }
                        </style>
                        """, unsafe_allow_html=True)

                        if (st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] != None):
                            ind_val = [i for i in range(1,11)].index(st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"])
                        else:
                            ind_val = None
                            
                        st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] = st.selectbox("", placeholder='Select Magnitude', options=[i for i in range(1,11)], index = ind_val, key=f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}_2")

                        criteria_df_list.append(st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] )
                    
                        if (st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] != None) and (st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"] != None):

                            criteria_df = pd.DataFrame(criteria_df_list).T
                            criteria_df.columns = st.session_state.ahp_selection_df.columns

                            st.session_state.ahp_selection_df = pd.concat([st.session_state.ahp_selection_df, criteria_df]).reset_index(drop = True)
                            
                            if combinations[i][0] == st.session_state[f"ahp_better_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"]:
                                matrix[combinations[i][0]][combinations[i][1]] = 1/st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"]
                            else:
                                matrix[combinations[i][0]][combinations[i][1]] = st.session_state[f"ahp_magnitude_dropdown_{team}_{combinations[i], model_id, st.session_state.user_name}"]
        
                            matrix[combinations[i][1]][combinations[i][0]] = 1/matrix[combinations[i][0]][combinations[i][1]]
    
                        else:
                            matrix[combinations[i][1]][combinations[i][0]] = None
                            matrix[combinations[i][0]][combinations[i][1]] = None
             
            st.markdown("<hr>", unsafe_allow_html=True)
    
        if matrix.isnull().any().any() == False:
            matrix['Geo Mean'] = matrix[variables].apply(get_gmean, axis=1)
            matrix['Weights'] = matrix['Geo Mean']/matrix['Geo Mean'].sum()
            matrix['1/sum'] = matrix[variables].apply(lambda row: sum(1/x for x in row if x != 0), axis=1)
            matrix['lmax'] = matrix['1/sum']*matrix['Weights']
    
            consistency_index = (np.sum(matrix['lmax']) - len(variables))/(len(variables) - 1)

            ri_lookup = pd.read_excel('RI Lookup.xlsx')
            random_index = ri_lookup[ri_lookup['Size'] == len(variables)]['RI'].iloc[0] # 0.58
            consistency_ratio = consistency_index/random_index
            
            # st.write(matrix)
            # st.write('Consistency Index:', consistency_index)
            # st.write('Random Index:', random_index)
            # st.write('Consistency Ratio:', consistency_ratio)

            for var in variables:

                if level == 'L2':
                    temp_df = pd.DataFrame([model_id, team, level, var, None, None, matrix['Weights'][var]]).T
        
                elif level == 'L3':
                    temp_df = pd.DataFrame([model_id, team, level, cat, var, None, matrix['Weights'][var]]).T
        
                elif level == 'L4':
                    temp_df = pd.DataFrame([model_id, team, level, cat, sub_cat, var, matrix['Weights'][var]]).T
                    
                temp_df.columns = st.session_state[f'ahp_weights_{team}'].columns
                st.session_state[f'ahp_weights_{team}'] = pd.concat([st.session_state[f'ahp_weights_{team}'], temp_df]).reset_index(drop = True)
            
            if consistency_ratio >= 0.1:
                st.markdown(f"""<div style='padding-left: 5px; background-color: #FFE7E7; color: #6E0202; padding-top: 1px; border-radius: 5px;'>
                    <p style='font-size: 13px; margin: 0;'><span>The responses are inconsistent.</span></p>
                    <p style='font-size: 13px; margin: 0;'>Consistency Ratio is <strong>{round(consistency_ratio, 3)}</strong>, which should be less than 0.1.</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state[f"ahp_consistency_check_{team}_{variables}_{model_id}_{st.session_state.user_name}"] = False
    
            else:
                if random_index == 0:
                    st.markdown(f"<div style='font-size: 13px; padding-left: 5px; background-color: #CFF4D0; color: green; padding-top: 1px; border-radius: 2px;'>The responses are consistent, as there are only 2 variables to analyse.</div>", unsafe_allow_html=True)

                else:
                    st.markdown(f"<div style='font-size: 13px; padding-left: 5px; background-color: #CFF4D0; color: green; padding-top: 1px; border-radius: 2px;'>The responses are consistent, with consistency ratio of <strong>{round(consistency_ratio, 3)}</strong>.</div>", unsafe_allow_html=True)
                st.session_state[f"ahp_consistency_check_{team}_{variables}_{model_id}_{st.session_state.user_name}"] = True


def get_gmean(x):
    if None not in list(x):
        x = x.astype(float)
        return np.exp(np.mean(np.log(x)))
    else:
        return None


































































def weights_display(weights_df, header, header_background_color, container_width):
    st.markdown(f"""
    <style>
    .heading-{header.split(' ')[0]} {{
            font-size: 17px;
            background-color: {header_background_color};
            color: white;
            padding-left: 5px;
            text-align: left;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: -10px;  # Corrected to a single margin-bottom property
    }}
    .centered {{
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        # background-color: grey;
        font-size: 15px;  # Uncommented and assumed you want it active
    }}
    hr {{
        margin-top: 0px;
        margin-bottom: 0px;
        height: 0.1px;
        background-color: #c2bfba; 
    }}
    .boldhr {{
        width: 100%;
        height: 2px;
        background-color: #9c9b99;
        margin: 2px;  # Uncommented and assumed you want it active
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="heading-{header.split(' ')[0]}">{header}</div>', unsafe_allow_html=True)
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)
    df_cols = weights_df.columns
    cols = st.columns(container_width)
    
    for i, label in enumerate(df_cols):
        with cols[i]:
            st.markdown(f"<div class='centered' style='font-weight: bold; margin-top: 0px'>{label}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # st.write(df_cols, weights_df)
 
    for i in range(0, len(weights_df)):
        cols = st.columns(container_width)
        for j in range(0, len(cols)):
            with cols[j]:
                if 'Weight' in df_cols[j]:
                    st.markdown(f"<div class='centered' style='margin-top: -10px; font-size: 15px;'>{round(weights_df[df_cols[j]][i], 4)}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='centered' style='margin-top: -10px font-size: 15px;'>{weights_df[df_cols[j]][i]}</div>", unsafe_allow_html=True)

        if i != len(weights_df) - 1:
            st.markdown("<hr>", unsafe_allow_html=True)
    st.write('\n')

def show_ahp_weight(team, df):
    
    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 80%;
        padding-left: 1%;
        padding-right: 1%;
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        margin-bottom: 0px;}
        
    .small-font {
        font-size:20px !important;
        # font-weight: bold;
        margin-bottom: -10px !important;
    }
    .boldhr {
        width: 100%;
        height: 1px;
        background-color: #9c9b99;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
     
    st.markdown(f'<p class="big-font">Verify Weights</p>', unsafe_allow_html=True)

    weights_final_df, l2_weights, l3_weights, av_l4_weights, bv_l4_weights, af_l4_weights, ewi_l4_weights = transfrom_and_load_weights(df, team)

    st.markdown(f'<p class="small-font">Application Variables</p>', unsafe_allow_html=True)
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    
    weights_display(l2_weights, 'L2 Weights', '#5e85b3', [1, 1, 1, 1])
    weights_display(l3_weights, 'L3 Weights', '#5e85b3', [1, 1, 1, 1, 1])
    weights_display(av_l4_weights, 'L4 Weights', '#5e85b3', [1, 1, 2, 2, 2, 1])
    weights_display(weights_final_df, 'Final Weights', '#5e85b3', [1, 1, 2, 1, 2, 1, 2, 1, 1])

    weights_final_df = pd.concat([weights_final_df, bv_l4_weights, af_l4_weights, ewi_l4_weights]).reset_index(drop = True)
    
    st.markdown(f'<p class="small-font">Behavioral Variables</p>', unsafe_allow_html=True)
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    weights_display(bv_l4_weights[['Model ID', 'Team', 'Variable Name', 'L4 Weight']], 'L4 Weights', '#5e85b3', [1, 1, 1, 1])
    
    st.markdown(f'<p class="small-font">Adjustments / Downgrade Factors</p>', unsafe_allow_html=True)
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    weights_display(af_l4_weights[['Model ID', 'Team', 'Variable Name', 'L4 Weight']], 'L4 Weights', '#5e85b3', [1, 1, 1, 1])
    
    st.markdown(f'<div class="small-font">Early Warning Indicators</div>', unsafe_allow_html=True)
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    weights_display(ewi_l4_weights[['Model ID', 'Team', 'Variable Name', 'L4 Weight']], 'L4 Weights', '#5e85b3', [1, 1, 1, 1])
    
    # st.markdown(f'<p class="small-font">Application Variables</p>', unsafe_allow_html=True)
    # st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    
    # weights_display(l2_weights, 'L2 Weights', '#965649', [1, 1, 1, 1])
    # weights_display(l3_weights, 'L3 Weights', '#968f4a', [1, 1, 1, 1, 1])
    # weights_display(av_l4_weights, 'L4 Weights', '#679649', [1, 1, 2, 2, 2, 1])
    # weights_display(weights_final_df, 'Final Weights', '#499657', [1, 1, 2, 1, 2, 1, 2, 1, 1])

    # weights_final_df = pd.concat([weights_final_df, bv_l4_weights, af_l4_weights, ewi_l4_weights]).reset_index(drop = True)
    
    # st.markdown("""
    # <style>
    # # div.stButton > button:first-child {
    # #     width: 250px; /* Set the width of the button */
    # #     background-color: #2E2E38; /* Change background to blue */
    # #     color: white; /* Change text color to white */
        
    # # }
    # /* Add CSS for centering the button */
    # div.stButton {
    #     display: flex;
    #     justify-content: center; /* Align button horizontally center */
    #     # margin: 10px 0; /* Optional: adds some space around the button */
    # }
    # </style>
    # """, unsafe_allow_html=True)
    
    if f'submit_ahp_weight_{team}' not in st.session_state:
        st.session_state[f'submit_ahp_weight_{team}'] = False
    
    if f'submit_ahp_weight_exp_run_{team}' not in st.session_state:
        st.session_state[f'submit_ahp_weight_exp_run_{team}'] = 0
        
    if st.session_state[f'submit_ahp_weight_{team}'] == False:
        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='verify_weight_back'):
            st.session_state['page'] = 'ahp_questionnaire'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()

        with cols_button[3]:

            st.markdown("""
            <style>
            .stPopoverBody {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding-bottom: 0px;
            width: 100%;
            }
            p, ol, ul, dl {
                font-size: 14px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with stylable_container(
                key="deploy_popover",
                css_styles="""
                    button {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-top: -15px;
                        width: 100%;
                        color: black;
                        font-size: 14px;
                        background-color: #b3c3d9;
                        border-radius: 50px;
                    }
                    """,
            ):
            
                with st.popover("Submit Response"):
                    st.markdown(f"<div class='stPopoverBody'>Are you sure you want to submit?</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='stPopoverBody'>Changes can not be made later.</div>", unsafe_allow_html=True)

                    yes_button = st.columns([1, 2, 1])
                    ChangeButtonColour('Yes', 'black', '#b3c3d9', '20px', margin_top = '10px', margin_bottom = '-20px')
                    if yes_button[1].button('Yes', key='verify_weight_back_ahp_q'):
                        
                        st.session_state[f'submit_ahp_weight_{team}'] = True 
                        
                        final_weights_ex = pd.read_excel('Weights.xlsx', sheet_name = 'Final Weights')
                        l2_weights_ex = pd.read_excel('Weights.xlsx', sheet_name = 'L2 Weights')
                        l3_weights_ex = pd.read_excel('Weights.xlsx', sheet_name = 'L3 Weights')
                        av_l4_weights_ex = pd.read_excel('Weights.xlsx', sheet_name = 'L4 Weights')
                
                        weights_final_df.insert(0, 'DateTime', [datetime.now()]*len(weights_final_df))
                        l2_weights.insert(0, 'DateTime', [datetime.now()]*len(l2_weights))
                        l3_weights.insert(0, 'DateTime', [datetime.now()]*len(l3_weights))
                        av_l4_weights.insert(0, 'DateTime', [datetime.now()]*len(av_l4_weights))
                
                        weights_final_df.insert(2, 'User', [st.session_state.email]*len(weights_final_df))
                        l2_weights.insert(2, 'User', [st.session_state.email]*len(l2_weights))
                        l3_weights.insert(2, 'User', [st.session_state.email]*len(l3_weights))
                        av_l4_weights.insert(2, 'User', [st.session_state.email]*len(av_l4_weights))
                
                        weights_final_df.insert(2, 'Product', [st.session_state.product]*len(weights_final_df))
                        l2_weights.insert(2, 'Product', [st.session_state.product]*len(l2_weights))
                        l3_weights.insert(2, 'Product', [st.session_state.product]*len(l3_weights))
                        av_l4_weights.insert(2, 'Product', [st.session_state.product]*len(av_l4_weights))
                        
                        final_weights_ex = pd.concat([final_weights_ex, weights_final_df], ignore_index=True)
                        with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            final_weights_ex.to_excel(writer, sheet_name='Final Weights', index=False)
                            
                        l2_weights_ex = pd.concat([l2_weights_ex, l2_weights], ignore_index=True)
                        with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            l2_weights_ex.to_excel(writer, sheet_name='L2 Weights', index=False)
                
                        l3_weights_ex = pd.concat([l3_weights_ex, l3_weights], ignore_index=True)
                        with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            l3_weights_ex.to_excel(writer, sheet_name='L3 Weights', index=False)
                
                        av_l4_weights_ex = pd.concat([av_l4_weights_ex, av_l4_weights], ignore_index=True)
                        with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            av_l4_weights_ex.to_excel(writer, sheet_name='L4 Weights', index=False)
                
                        assigned_forms = pd.read_excel('assign_forms.xlsx')
                        assigned_forms.loc[((assigned_forms['model_id'] == st.session_state.model_id) & 
                                    (assigned_forms['product'] == st.session_state.product) & 
                                    (assigned_forms['team'] == st.session_state.team) & 
                                    (assigned_forms['user'] == st.session_state.email) & 
                                    (assigned_forms['questionnaire'] == 'AHP')), 'completed'] = 1
                
                        
                        assigned_forms.loc[((assigned_forms['model_id'] == st.session_state.model_id) & 
                                    (assigned_forms['product'] == st.session_state.product) & 
                                    (assigned_forms['team'] == st.session_state.team) & 
                                    (assigned_forms['user'] == st.session_state.email) & 
                                    (assigned_forms['questionnaire'] == 'AHP')), 'reviewed'] = 1
                        
                        with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            assigned_forms.to_excel(writer, sheet_name='Sheet1', index=False)
            
                        ahp_selection = pd.read_excel('AHP Selection.xlsx')
            
                        ahp_selection = pd.concat([ahp_selection, st.session_state.ahp_selection_df]).reset_index(drop = True)
                        ahp_selection.to_excel('AHP Selection.xlsx', index=False)
                        
    col1, col2, col3 = st.columns(3)
    with col2:
        if (st.session_state[f'submit_ahp_weight_{team}'] == True):
            st.markdown("""
    <div style='text-align: center; background-color: #CFF4D0; color: green; padding-top: 15px; padding-bottom: 1px; border-radius: 5px;'>
        <p>✅ The response has been submitted successfully.</p>
    </div>
    """, unsafe_allow_html=True)

            st.session_state['page'] = 'pending_page_user'
            
            if st.session_state[f'submit_ahp_weight_exp_run_{team}'] == 0:
                st.session_state[f'submit_ahp_weight_exp_run_{team}'] += 1
                
                st.session_state.need_rerun = True
                st.session_state.need_rerun = False
                st.rerun()


def transfrom_and_load_weights(df, team):
    df['Sub-category'].fillna(df['Category'], inplace=True)
    
    l2_weights = df[df['Level'] == 'L2'][['Category', 'Weight']].rename(columns={'Weight': 'L2 Weight'}).drop_duplicates().reset_index(drop = True)
    l3_weights = df[df['Level'] == 'L3'][['Category', 'Sub-category', 'Weight']].rename(columns={'Weight': 'L3 Weight'}).drop_duplicates().reset_index(drop = True)
    l4_weights = df[df['Level'] == 'L4'][['Category', 'Sub-category', 'Variable Name', 'Weight']].rename(columns={'Weight': 'L4 Weight'}).drop_duplicates().reset_index(drop = True)
    
    result = l2_weights.merge(l3_weights, 
                              how = 'left', 
                              on = 'Category').merge(l4_weights,
                                                    how = 'left',
                                                    on = ['Category', 'Sub-category'])
    result['Final Weight'] = result['L2 Weight']*result['L3 Weight']*result['L4 Weight']

    l2_weights.insert(0, 'Team', [team]*len(l2_weights))
    l2_weights.insert(0, 'Model ID', [st.session_state['model_id']]*len(l2_weights))
    
    l3_weights.insert(0, 'Team', [team]*len(l3_weights))
    l3_weights.insert(0, 'Model ID', [st.session_state['model_id']]*len(l3_weights))
    
    l4_weights.insert(0, 'Team', [team]*len(l4_weights))
    l4_weights.insert(0, 'Model ID', [st.session_state['model_id']]*len(l4_weights))
    
    result.insert(0, 'Team', [team]*len(result))
    result.insert(0, 'Model ID', [st.session_state['model_id']]*len(result))

    av_l4_weights =  l4_weights[~l4_weights['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])].reset_index(drop = True)

    bv_l4_weights =  l4_weights[l4_weights['Category'] == 'Behavioral Variables'].reset_index(drop = True)
    bv_l4_weights['L2 Weight'] = 1
    bv_l4_weights['L3 Weight'] = 1
    bv_l4_weights['Final Weight'] = bv_l4_weights['L2 Weight']*bv_l4_weights['L3 Weight']*bv_l4_weights['L4 Weight']

    af_l4_weights =  l4_weights[l4_weights['Category'] == 'Adjustments / Downgrade Factors'].reset_index(drop = True)
    af_l4_weights['L2 Weight'] = 1
    af_l4_weights['L3 Weight'] = 1
    af_l4_weights['Final Weight'] = af_l4_weights['L2 Weight']*af_l4_weights['L3 Weight']*af_l4_weights['L4 Weight']

    ewi_l4_weights =  l4_weights[l4_weights['Category'] == 'Early Warning Indicators'].reset_index(drop = True)
    ewi_l4_weights['L2 Weight'] = 1
    ewi_l4_weights['L3 Weight'] = 1
    ewi_l4_weights['Final Weight'] = ewi_l4_weights['L2 Weight']*ewi_l4_weights['L3 Weight']*ewi_l4_weights['L4 Weight']
    
    return result, l2_weights, l3_weights, av_l4_weights, bv_l4_weights, af_l4_weights, ewi_l4_weights
















































def ahp_weights_agg(model_id):
    st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 90%;
        padding-left: 1%;
        padding-right: 1%;
    }
    .big-font {
            font-size:30px !important;
            font-weight: bold;
            margin-bottom: 0px;
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    # img_title("EY Logo.png")
    
    st.markdown(f'<p class="big-font">AHP Weights Aggregation</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Product: {st.session_state.product}</p>', unsafe_allow_html=True)
    # st.write('\n')
    st.markdown("""
    <style>
    .heading {
        font-size: 20px;
        background-color: #968f4a;
        color: white;
        padding: 5px;
        text-align: left;
        border-radius: 5px;
        cursor: pointer;
    }
    .hr-short {
        margin-top: 0px;
        margin-bottom: 0px;
        height: 2px; /* Adjust height to make the dotted line more visible */
        border-top: 3px dotted #9c9b99; /* Apply dotted style */
        background: transparent; /* Ensure the background does not interfere */
        width: 55%;  /* Adjust the width as needed */
        border-bottom: none; /* Remove bottom border if any */
    }
    hr {
        margin-top: 0px;
        margin-bottom: 0px;
        height: 0.1px;
        background-color: #9c9b99;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="heading">Select Weights for Teams</div>', unsafe_allow_html=True)

    weights_excel = pd.read_excel('Weights.xlsx', sheet_name = 'Final Weights')
    Users = pd.read_excel('Users.xlsx')
    weights_df = weights_excel[weights_excel['Model ID'] == model_id].reset_index(drop = True).merge(Users[['email', 'f_name', 'l_name']],
                                                                                                     how = 'left',
                                                                                                     left_on = 'User', 
                                                                                                     right_on = 'email').drop('email', axis = 1)

    weights_df['user_name_team'] = weights_df['f_name'].fillna('') + ' ' + weights_df['l_name'].fillna('') + ' (' + weights_df['Team'].fillna('') + ')'

    

    teams = list(pd.unique(weights_df['user_name_team']))
    teams_weights = []

    # st.write(weights_df)

    for i in range(0, len(teams)):
        if f"ahp_agg_team_weight_{teams[i]}" not in st.session_state:
            st.session_state[f"ahp_agg_team_weight_{teams[i]}"] = 1

    teams_weights_sum = sum([st.session_state[key] for key in st.session_state if key.startswith(f"ahp_agg_team_weight_")])
    # teams_weights_sum
    
    for i in range(0, len(teams)):
        cols = st.columns([1.5, 10, 10, 10, 10])
        
        with cols[2]:
            teams_weights.append(st.selectbox('', placeholder='Select Weight', options=[j for j in range(1,11)], index = 0, key=f"ahp_agg_team_weight_{teams[i]}"))

        with cols[1]:
            team_weight_perc = round(100*st.session_state[f"ahp_agg_team_weight_{teams[i]}"]/teams_weights_sum, 2)
            
            st.markdown("""<style>.stSelectbox {margin-top: -20px;}</style>""", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 20px;'><p>Select Weight for {teams[i]} ({team_weight_perc}%): </p></div>", unsafe_allow_html=True)

        if i != len(teams) - 1:
            st.markdown('<hr class="hr-short">', unsafe_allow_html=True)

    cols = ['Category', 'Sub-category', 'Variable Name'] + teams + ['Weight Agg']

    weights_agg_df = pd.DataFrame(columns = cols)
    
    weights_agg_df = weights_df.loc[weights_df['user_name_team'] == teams[0]][['Category', 'Sub-category', 'Variable Name', 'Final Weight']]
    weights_agg_df[f'Weighted {teams[0]}'] = weights_agg_df['Final Weight']*teams_weights[0]/np.sum(teams_weights)
    
    weights_agg_df.rename(columns={'Final Weight': f'Weight {teams[0]}'}, inplace=True)
    team_weight_cols = [f'Weighted {teams[0]}']
    
    weight_cols = [f'Weight {teams[0]}']

    for i in range(1, len(teams)):
        weights_agg_df = weights_agg_df.merge(weights_df.loc[weights_df['user_name_team'] == teams[i]][['Category', 'Sub-category', 'Variable Name', 'Final Weight']],
                                              how = 'left',
                                              on  = ['Category', 'Sub-category', 'Variable Name']).reset_index(drop = True)
        weights_agg_df[f'Weighted {teams[i]}'] = weights_agg_df['Final Weight']*teams_weights[i]/np.sum(teams_weights)
        
        weights_agg_df.rename(columns={'Final Weight': f'Weight {teams[i]}'}, inplace=True)
        
        weight_cols.append(f'Weight {teams[i]}')
        team_weight_cols.append(f'Weighted {teams[i]}')
        
    weights_agg_df['Weight Agg'] = weights_agg_df[team_weight_cols].sum(axis = 1)
    weights_agg_df.insert(0, 'Model ID', model_id)

    weights_agg_df_av = weights_agg_df[~weights_agg_df['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])].reset_index(drop = True)
    weights_agg_df_bv = weights_agg_df[weights_agg_df['Category'] == 'Behavioral Variables'].reset_index(drop = True)
    weights_agg_df_baf = weights_agg_df[weights_agg_df['Category'] == 'Adjustments / Downgrade Factors'].reset_index(drop = True)
    weights_agg_df_ewi = weights_agg_df[weights_agg_df['Category'] == 'Early Warning Indicators'].reset_index(drop = True)

    weights_display(weights_agg_df_av[['Category', 'Sub-category', 'Variable Name'] + weight_cols + ['Weight Agg']], 'Application Variables - Aggregated Weights', '#65964a', [1.1, 1.1, 1.1] + len(weight_cols)*[1] + [1]) 

    weights_display(weights_agg_df_bv[['Category', 'Sub-category', 'Variable Name'] + weight_cols + ['Weight Agg']], 'Behavioral Variables - Aggregated Weights', '#858758', [1.1, 1.1, 1.1] + len(weight_cols)*[1] + [1])

    weights_display(weights_agg_df_baf[['Category', 'Sub-category', 'Variable Name'] + weight_cols + ['Weight Agg']], 'Adjustments / Downgrade Factors - Aggregated Weights', '#85625b', [1.1, 1.1, 1.1] + len(weight_cols)*[1] + [1])

    weights_display(weights_agg_df_ewi[['Category', 'Sub-category', 'Variable Name'] + weight_cols + ['Weight Agg']], 'Early Warning Indicators - Aggregated Weights', '#965649', [1.1, 1.1, 1.1] + len(weight_cols)*[1] + [1])

    st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 250px; /* Set the width of the button */
        background-color: #2E2E38; /* Change background to blue */
        color: white; /* Change text color to white */
        
    }
    /* Add CSS for centering the button */
    div.stButton {
        display: flex;
        justify-content: center; /* Align button horizontally center */
        margin: 10px 0; /* Optional: adds some space around the button */
    }
    </style>
    """, unsafe_allow_html=True)
    
    if f'weights_agg_{model_id}' not in st.session_state:
        st.session_state[f'weights_agg_{model_id}'] = False

    if f'submit_ahp_weight_agg_exp_run_{model_id}' not in st.session_state:
        st.session_state[f'submit_ahp_weight_agg_exp_run_{model_id}'] = 0

    if st.session_state[f'weights_agg_{model_id}'] == False:

        cols_button = st.columns(6)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px')
        if cols_button[2].button('Back', key='agg_back_home'):
            st.session_state['page'] = 'admin_models'
            st.session_state.admin_model_tabs = 3
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()


        with cols_button[3]:

            st.markdown("""
            <style>
            .stPopoverBody {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding-bottom: 0px;
            width: 100%;
            }
            p, ol, ul, dl {
                font-size: 14px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            with stylable_container(
                key="deploy_popover",
                css_styles="""
                    button {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-top: -6px;
                        width: 100%;
                        color: black;
                        font-size: 14px;
                        background-color: #b3c3d9;
                        border-radius: 50px;
                    }
                    """,
            ):
            
                with st.popover("Submit Weights"):
                    st.markdown(f"<div class='stPopoverBody'>Are you sure you want to submit?</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='stPopoverBody'>Changes can not be made later.</div>", unsafe_allow_html=True)

                    yes_cols = st.columns([1, 2, 1])
                    ChangeButtonColour('Yes', 'black', '#b3c3d9', '20px', margin_bottom = '-40px')
                    if yes_cols[1].button('Yes', key='submit_agg_weights'):
                        st.session_state[f'weights_agg_{model_id}'] = True
                        
                        weights_agg_df['Active'] = 1
                        
                        weights_agg_ex = pd.read_excel('Weights.xlsx', sheet_name = 'Weights Agg')
                        weights_agg_ex.loc[weights_agg_ex['Product'] == st.session_state.product, 'Active'] = 0
                        
                        weights_agg_df.insert(0, 'DateTime', [datetime.now()]*len(weights_agg_df))
                        weights_agg_df.insert(2, 'Product', st.session_state.product)
                
                        weights_to_load = weights_agg_df[['DateTime', 'Model ID', 'Product', 'Category', 'Sub-category', 'Variable Name', 'Weight Agg', 'Active']]
                        weights_to_load.rename(columns={'Weight Agg': 'Weight'}, inplace=True)
                        
                        weights_agg_ex = pd.concat([weights_agg_ex, weights_to_load], ignore_index=True)
            
                        with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            weights_agg_ex.to_excel(writer, sheet_name='Weights Agg', index=False)
            
                        assigned_forms = pd.read_excel('assign_forms.xlsx')
                            
                        assigned_forms.loc[((assigned_forms['model_id'] == st.session_state.model_id) & 
                                            (assigned_forms['product'] == st.session_state.product) & 
                                            (assigned_forms['questionnaire'] == 'Aggregation')), 'completed'] = 1
                        
                        assigned_forms.loc[((assigned_forms['model_id'] == st.session_state.model_id) & 
                                            (assigned_forms['product'] == st.session_state.product) & 
                                            (assigned_forms['questionnaire'] == 'Aggregation')), 'reviewed'] = 1
            
                        with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            assigned_forms.to_excel(writer, sheet_name='Sheet1', index=False)



                        
                        
                        model_state = pd.read_excel('assign_forms.xlsx', sheet_name = 'model_state')
                        temp_model_state_list = [datetime.now(), st.session_state.model_id, st.session_state.product, 1]
                        temp_model_state_df = pd.DataFrame(temp_model_state_list).T
                        temp_model_state_df.columns = model_state.columns
            
                        model_state.loc[(model_state['product'] == st.session_state.product), 'active'] = 0
                        model_state = pd.concat([model_state, temp_model_state_df], ignore_index=True)
            
                        with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            model_state.to_excel(writer, sheet_name='model_state', index=False)



                        
            

                        st.session_state['page'] = 'admin_models'
                        
                        st.session_state.need_rerun = True
                        if st.session_state.need_rerun:
                            st.session_state.need_rerun = False
                            st.rerun()







