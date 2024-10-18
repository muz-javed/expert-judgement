import re
import time
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container

# from functions_model_development import combine_comments


def initialize_states():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if 'user_name' not in st.session_state:
        st.session_state.user_name = None

    if 'email' not in st.session_state:
        st.session_state.email = None

    if 'team' not in st.session_state:
        st.session_state.team = None

def login_screen():
    login_cols = st.columns([1, 3, 1])
    with login_cols[1]:    
        css = """
        <style>
            .stApp {
                background-color: #b3c3d9;
            }
            .css-18e3th9 {
                background-color: #b3c3d9;
            }
        </style>
        """
         
        st.markdown(css, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="border-radius: 5px; margin-top: 20px; margin-bottom: -100px;">
                <h3 style="text-align:center; color: black; font-weight: bold;">Constrained Expert Judgement Modelling Tool</h3>
            </div>
            """, unsafe_allow_html=True)
        
        main_cols = st.columns([1, 9, 1])
        with main_cols[1]:
            st.markdown(f"""
            <div style="background-color: #F0F2F6; padding: 10px; border-radius: 10px; margin-top: 100px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <h2 style="text-align:left; font-size:25px ;color: black; padding-left: 65px; margin-top:20px; margin-bottom:250px;">Login</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <style>
                    div[data-baseweb="input"] input {
                        background-color: inherit !important;  /* Ensures background color is inherited */
                        color: black !important;              /* Sets text color */
                        border: none !important;              /* Removes borders */
                        border-radius: 0px !important;        /* Removes border radius */
                        outline: none !important;             /* Removes focus outline */
                    }
                
                    div[data-baseweb="input"] input:focus {
                        border: none !important;              /* Reinforces no border on focus */
                        outline: none !important;             /* Reinforces no outline on focus */
                    }
                
                    div[data-baseweb="input"] input::placeholder {
                        color: #a6a6a6 !important;            /* Custom placeholder text color, force override */
                    }
                
                    .stTextInput {
                        margin-top: -280px;                   /* Adjust the negative margin as needed */
                    }
                
                    .divider {
                        height: 0.1px;
                        background-color: black;
                        margin-top: -230px;
                    }
                </style>
                """, unsafe_allow_html=True)
            
            cols = st.columns([1, 6, 1])
            with cols[1]:
                email_id = st.text_input(label = 'Username/Email ID', placeholder = 'Enter Email ID', key='e_id')
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.write('\n')
                st.write('\n')
                st.write('\n')
            with cols[1]:
                password = str(st.text_input(label = "Password", placeholder = 'Enter Password', type='password', key='pwd'))
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.write('\n')
                st.write('\n')
                st.write('\n')
            with cols[1]:
                # st.markdown("""
                # <style>
                # div.stButton > button:first-child {
                #     background-color: black; ##42638f; 
                #     color: white; 
                #     width: 100%;
                #     border-radius: 100px;
                    
                # }
                # /* Add CSS for centering the button */
                # div.stButton {
                #     display: flex;
                #     justify-content: center; /* Align button horizontally center */
                #     margin-top: -280px; /* Optional: adds some space around the button */
                # }
                # </style>
                # """, unsafe_allow_html=True)
    
    
                ChangeButtonColour('Login', 'white', 'black', '20px', margin_top = '-300px', margin_bottom = '-300px')
                if cols[1].button('Login', key='login'):
                # if st.button('Login'):
                    if 'users' not in st.session_state:
                        st.session_state.users = pd.read_excel('Users.xlsx')
                        
                    st.session_state.users['password'] = st.session_state.users['password'].astype(str)
                        
                    if (email_id in list(st.session_state.users['email'])) and (st.session_state.users[st.session_state.users['email'] == email_id]['password'].iloc[0] == password):
    
                        st.session_state.user_name = f'{st.session_state.users[st.session_state.users['email'] == email_id]['f_name'].iloc[0]} {'' if pd.isna(st.session_state.users[st.session_state.users['email'] == email_id]['l_name'].iloc[0]) else st.session_state.users[st.session_state.users['email'] == email_id]['l_name'].iloc[0]}'
                        
                        st.session_state.email = email_id
                        st.session_state.team = st.session_state.users[(st.session_state.users['email'] ==  email_id)]['team'].iloc[0]
                        
                        if st.session_state.users[st.session_state.users['email'] == email_id]['role'].iloc[0] == 'Admin':
                            st.session_state.page = 'admin_home'
                            st.session_state.need_rerun = True
                            if st.session_state.need_rerun:
                                st.session_state.need_rerun = False
                                st.rerun()
    
                        if st.session_state.users[st.session_state.users['email'] == email_id]['role'].iloc[0] == 'User':
                            st.session_state.page = 'pending_page_user'
                            st.session_state.need_rerun = True
                            if st.session_state.need_rerun:
                                st.session_state.need_rerun = False
                                st.rerun()
    
                        if st.session_state.users[st.session_state.users['email'] == email_id]['role'].iloc[0] == 'CR':
                            st.session_state.page = 'cr_page'
                            st.session_state.need_rerun = True
                            if st.session_state.need_rerun:
                                st.session_state.need_rerun = False
                                st.rerun()
    
                    else:
                        
                        st.markdown(f"<div style='font-size: 11px; text-align: left;color: #ff8080;margin-top: -350px;'>Incorrect Username or Password.</div>", unsafe_allow_html=True)
    

def admin_sidebar():

    cols = st.columns([0.3, 4, 0.3])
    with cols[1]:
    
        with st.sidebar:
            css = """
            <style>
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #b3c3d9;  /* Change this color to any hex color you prefer */
            }
            </style>
            """
        
            st.markdown(css, unsafe_allow_html=True)
            st.write(f'Logged in as: \n{st.session_state.user_name}')
    
    
            # st.markdown("""
            # <style>
            #     div.stButton > button:first-child {
            #     background-color: #b3c3d9; /* Change background to blue */
            #     color: black; /* Change text color to white */
            #     border: none;
            #     margin-bottom: -50px;
            #     # text-decoration: underline; /* Add underline to the text */
                
            #     }
            #     /* Add CSS for centering the button */
            #     div.stButton {
            #         display: flex;
            #         justify-content: center; /* Align button horizontally center */
            #     }
            #     hr {
            #         margin-bottom: 0px;
            #         background-color: #9c9b99; 
            #     }
            #     </style>
            #     """, unsafe_allow_html=True)

            
            st.markdown("""
            <style>
                hr {
                    margin-top: -10px;
                    margin-bottom: -100px;
                    background-color: #9c9b99; 
                }
                </style>
                """, unsafe_allow_html=True)
            
            # st.markdown("<hr>", unsafe_allow_html=True)

            cols = st.columns([1, 8, 1])
            ChangeButtonColour('Home', 'black', '#b3c3d9', '20px', margin_top = '-10px', margin_bottom = '-300px')
            if cols[1].button('Home', key='admin_home'):
                
            # if st.button('Home'):
                st.session_state.page = 'admin_home'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()
                    
            # st.markdown("<hr>", unsafe_allow_html=True)
            cols = st.columns([1, 8, 1])
            ChangeButtonColour('Models', 'black', '#b3c3d9', '20px', margin_top = '-10px', margin_bottom = '-300px')
            if cols[1].button('Models', key='admin_models'):
            # if st.button('Models'):
                st.session_state.page = 'admin_models'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()
                    
            # st.markdown("<hr>", unsafe_allow_html=True)
            cols = st.columns([1, 8, 1])
            ChangeButtonColour('Roles', 'black', '#b3c3d9', '20px', margin_top = '-10px', margin_bottom = '-300px')
            if cols[1].button('Roles', key='admin_roles'):
            # if st.button('Roles'):
                st.session_state.page = 'admin_roles'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()

            # st.markdown("<hr>", unsafe_allow_html=True)
            cols = st.columns([1, 8, 1])
            ChangeButtonColour('Logout', 'black', '#b3c3d9', '20px', margin_top = '-10px', margin_bottom = '-300px')
            if cols[1].button('Logout', key='admin_logout'):
            # if st.button('Logout'):
                st.session_state.page = 'login'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()
            # st.markdown("<hr>", unsafe_allow_html=True)


def cr_sidebar():

    cols = st.columns([0.3, 4, 0.3])
    with cols[1]:
    
        with st.sidebar:
            css = """
            <style>
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #b3c3d9;  /* Change this color to any hex color you prefer */
            }
            </style>
            """
        
            st.markdown(css, unsafe_allow_html=True)
            st.write(f'Logged in as: \n{st.session_state.user_name}')
    
    
            # st.markdown("""
            # <style>
            #     div.stButton > button:first-child {
            #     background-color: #b3c3d9; /* Change background to blue */
            #     color: black; /* Change text color to white */
            #     border: none;
            #     margin-bottom: -50px;
            #     # text-decoration: underline; /* Add underline to the text */
                
            #     }
            #     /* Add CSS for centering the button */
            #     div.stButton {
            #         display: flex;
            #         justify-content: center; /* Align button horizontally center */
            #     }
            #     hr {
            #         margin-bottom: 0px;
            #         background-color: #9c9b99; 
            #     }
            #     </style>
            #     """, unsafe_allow_html=True)

            cols = st.columns([1, 8, 1])
            ChangeButtonColour('Logout', 'black', '#b3c3d9', '20px')
            if cols[1].button('Logout', key='admin_logout'):
            # if st.button('Logout'):
                st.session_state.page = 'login'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()

            # st.markdown("<hr>", unsafe_allow_html=True)
            # if st.button('Logout'):
            #     st.session_state.page = 'login'
            #     st.session_state.need_rerun = True
            #     if st.session_state.need_rerun:
            #         st.session_state.need_rerun = False
            #         st.rerun()
            # st.markdown("<hr>", unsafe_allow_html=True)


def ChangeButtonColour(widget_label, font_color, background_color='transparent', radius = '0px', disabled = False, margin_top='0px', margin_bottom='0px', margin_left='0px', justifyContent = 'center', text_decor = 'none', padding_left = '12px', padding_right = '12px', padding_top = '4px', padding_bottom = '4px', border=''):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    elements[i].style.width = '100%';
                    elements[i].style.textAlign = 'center';
                    elements[i].style.textDecoration = 'None';
                    elements[i].style.display = 'flex';
                    elements[i].style.justifyContent = '{justifyContent}';
                    elements[i].style.borderRadius = '{radius}';
                    elements[i].style.disabled = '{disabled}';
                    elements[i].style.marginBottom = '{margin_bottom}';
                    elements[i].style.marginTop = '{margin_top}';
                    elements[i].style.marginLeft = '{margin_left}';
                    elements[i].style.textDecoration = '{text_decor}';
                    elements[i].style.paddingLeft = '{padding_left}';
                    elements[i].style.paddingRight = '{padding_right}';
                    elements[i].style.paddingTop = '{padding_top}';
                    elements[i].style.paddingBottom = '{padding_bottom}';
                    elements[i].style.border = '{border}';
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)


def show_prompt_for_seconds(seconds, text, margin_top = '-40px'):
    placeholder = st.empty()
    
    placeholder.markdown(f"""
    <div style='text-align: left; padding-left:10px; background-color: #CFF4D0; color: green; border-radius: 5px;  margin-top: {margin_top};'>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(seconds)
    
    placeholder.empty()


def admin_home():
    st.markdown(f"""
    <div style="border-radius: 5px; margin-bottom: -60px;">
        <h2 style="text-align:left; color: black; font-weight: bold;">Home</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .main .block-container {
            max-width: 90%;
        }
    </style>
    """, unsafe_allow_html=True)
    
    admin_sidebar()
    
    st.image('home_page_overview.png')


    
def admin_roles():
    st.markdown(f"""
    <div style="border-radius: 5px;">
        <h2 style="text-align:left; color: black; font-weight: bold;">Roles</h2>
    </div>
    """, unsafe_allow_html=True)

    admin_sidebar()

    st.markdown("""
    <style>
    /* Flex container for tabs */

    /* Individual tabs */
    button[data-baseweb="tab"] {
        flex-grow: 1; /* Grow to fill space */
        text-align: center; /* Center text inside tabs */
    }
    .st-cr {
        color: black;
    }
    .st-d8 {
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    tabs = st.tabs(['Add New User', 'Existing Users'])


    if 'team' not in st.session_state:
        st.session_state.team = None
    if 'prod' not in st.session_state:
        st.session_state.prod = None
    if 'e_id' not in st.session_state:
        st.session_state.e_id = None
    if 'quest' not in st.session_state:
        st.session_state.quest = None

    with tabs[0]:
        all_users = pd.read_excel('Users.xlsx')
        
        cols = st.columns([0.3, 2, 2, 0.3])

        with cols[1]:
            
            st.write('Select Team:')
            st.write('\n')
            st.write('Select User:')
            st.write('\n')
            st.write('Select Product:')
            st.write('\n')
            st.write('Select Questionnaire:')

        with cols[2]:
            st.markdown("""
                <style>
                    .stSelectbox {
                        margin-top: -60px;
                    }
                </style>
                """, unsafe_allow_html=True)
            team = st.selectbox('', options = ['Credit', 'Credit Risk', 'Business', 'Policy & Portfolio'], index = None, key='team')
        
        with cols[2]:
            st.markdown("""
                <style>
                    .stTextInput {
                        margin-top: -48px;
                    }
                </style>
                """, unsafe_allow_html=True)
            options = all_users[all_users['team'] == team]
            if team == None:
                placeholder = 'Select User'
            elif len(options) == 0: 
                placeholder = f'No user(s) exists for {team} team.'
            else:
                placeholder = 'Select User'
            email_id = st.selectbox('', options = options, placeholder = placeholder, index = None, key='e_id')
        
        with cols[2]:
            st.markdown("""
                <style>
                    .stSelectbox {
                        margin-top: -42px;
                    }
                </style>
                """, unsafe_allow_html=True)
            prod_type = st.selectbox('', options = ['POS', 'CRE IPRE', 'MBBF IPRE', 'MBBF Business', 'Business Credit Card'], index = None, key='prod')

        with cols[2]:
            st.markdown("""
                <style>
                    .stSelectbox {
                        margin-top: -42px;
                    }
                </style>
                """, unsafe_allow_html=True)
            quest_type = st.selectbox('', options = ['AHP', 'Delphi'], index = None, key='quest')
            if quest_type == 'Delphi':
                enable_reviewer = False
                reviewer = None
            else:
                enable_reviewer = True
                reviewer = 'No'

        if enable_reviewer == False:
            with cols[1]:
                st.write('\n')
                st.write('Questionnaire Reviewer:')
            with cols[2]:
                st.markdown("""
                    <style>
                        .stSelectbox {
                            margin-top: -42px;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                reviewer = st.selectbox('', options = ['Yes', 'No'], index = None, key='reviewer')

        if (email_id not in list(pd.read_excel('Users.xlsx')['email'])) and (email_id != None):
            cols = st.columns([0.3, 4, 0.3])
            with cols[1]:
                st.markdown("""<div style='background-color: #FFE7E7; color: #6E0202; padding-left: 10px; border-radius: 3px;'><p>Email ID does not exist in the user database.</p></div>""", unsafe_allow_html=True)

        if (team != None) & (email_id != None) & (prod_type != None) & (quest_type != None) & (reviewer != None):
            disable_button = False
        else:
            disable_button = True
        
        cols = st.columns(3)
        ChangeButtonColour('Assign', 'black', '#b3c3d9', '20px', disable_button)
        if cols[1].button('Assign', key='b1', disabled = disable_button):
            
            roles_excel = pd.read_excel('Roles.xlsx')
            user_values = [email_id, prod_type, team, quest_type]
            match_users = roles_excel.apply(lambda row: list(row[:4]) == user_values, axis=1).any()
            reviewer_values = [prod_type, reviewer]
            match_reviewer = roles_excel.apply(lambda row: list(row[['Product', 'Reviewer']]) == reviewer_values, axis=1).any()

            if (match_users == True):
                cols = st.columns([0.3, 4, 0.3])
                with cols[1]:
                    st.markdown("""<div style='background-color: #FFE7E7; color: #6E0202; padding-left: 10px; border-radius: 3px; margin-top: -40px;'><p>User already exists for the above selection.</p></div>""", unsafe_allow_html=True)

            elif (quest_type == 'Delphi') and (reviewer == 'Yes') and (match_reviewer == True):
                cols = st.columns([0.3, 4, 0.3])
                with cols[1]:
                    st.markdown(f"""<div style='background-color: #FFE7E7; color: #6E0202; padding-left: 10px; border-radius: 3px; margin-top: -40px;'><p>Delphi reviewer already exists for {prod_type}.</p></div>""", unsafe_allow_html=True)

            else:
                temp_roles = [email_id, prod_type, team, quest_type, reviewer, datetime.now()]
                temp_roles = pd.DataFrame(temp_roles).T
                temp_roles.columns = roles_excel.columns
                
                roles_excel = pd.concat([roles_excel, temp_roles]).reset_index(drop = True)
                roles_excel.to_excel('Roles.xlsx', index=False)

                del st.session_state.team
                del st.session_state.e_id
                del st.session_state.prod
                del st.session_state.quest

                cols = st.columns([0.3, 4, 0.3])
                with cols[1]:
                    show_prompt_for_seconds(3, 'The role has been assigned successfully.')

                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()

    with tabs[1]:

        st.markdown("""
        <style>
        .main .block-container {
            max-width: 80%;
            # padding-left: 1%;
            # padding-right: 1%;
        }
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            margin-top: -30px;
            # padding-right: 10px;
            font-size: 14px;
        }
        .boldhr {
            width: 100%;
            height: 1px;
            background-color: #9c9b99; 
            # margin: 2px;
            margin-top: -20px;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    
        cols = st.columns([0.5, 0.6, 0.5, 0.4, 0.4, 0.5, 0.15])
        
        header_labels = ['Email ID', 'Product', 'Team',	'Questionnaire', 'Reviewer', 'Date Added At']
        
        for i, label in enumerate(header_labels):
            with cols[i]:
                st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 10px'>{label}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
        

        roles_ex = pd.read_excel('Roles.xlsx').sort_values('Product').reset_index(drop = True)
        for i in range(0, len(roles_ex)):
            cols = st.columns([0.5, 0.6, 0.5, 0.4, 0.4, 0.5, 0.15])

            if f'show_popover_{i}' not in st.session_state:
                st.session_state[f'show_popover_{i}'] = False
            # st.write(i)

            for j in range(0, 7):
                with cols[j]:
                    if j == 6:
                        st.markdown("""
                        <style>
                        .stPopoverBody {
                        margin: 0px;
                        padding: 0px;
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
                                            # margin-bottom: -300px;
                                            margin-top: -55px;
                                            margin-left: -15px;
                                            border: none;
                                            # color: #4088e6;
                                            font-size: 14px;
                                            # text-decoration: underline;
                                            background-color: transparent;
                                        }
                                        """,
                                ):
                        
                            with st.popover("🗑️"):
                                st.markdown(f"<div class='centered' style='margin-top: -10px'>Are you sure you want to delete?</div>", unsafe_allow_html=True)
                                # st.button('Yes', key = i)
                                cols_delete = st.columns(3)
                                ChangeButtonColour('Yes', 'black', '#b3c3d9', '5px', False, '5px', '-40px', '0px')
    
                                if cols_delete[1].button('Yes', key=f'{i}_delete'):
                                    st.session_state[f'show_popover_{i}'] = True
    
                                    roles_ex.drop(index = i).to_excel('Roles.xlsx', index=False)
        
                                    st.session_state.need_rerun = True
                                    if st.session_state.need_rerun:
                                        st.session_state.need_rerun = False
                                        st.rerun()
                                        
                    else:
                        if j == 5:
                            element = str(roles_ex[header_labels[j]][i]).split('.')[0]
                        else:
                            element = roles_ex[header_labels[j]][i]
                            
                        st.markdown(f"<div class='centered' style='margin-bottom: 10px'>{element}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 

def combine_relevance(group):
    return ' \n\n'.join(group['name_team'])

def combine_comments(group):
    return ' \n\n'.join(group['Labeled Comments'])

def combine_selection(group):
    return ' \n\n'.join(group['selection_name_team'])

def combine_magnitude(group):
    return ' \n\n'.join(group['magnitude_name_team'])

def model_report_ahp_weights(header, ahp_weights):
    st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-top: -20px;
        # margin-bottom: 40px;
        # padding-right: 10px;
        font-size: 14px;
    }
    .boldhr {
        width: 100%;
        height: 1.3px;
        background-color: #9c9b99; 
        margin: 2px;
        margin-top: -5px;
    }
    hr {
        margin-top: -6px;
        margin-bottom: 0px;
        background-color: white; 
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-weight: bold; font-size: 18px; margin-bottom: 4px;'>{header}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 

    cols = st.columns([2, 2, 2, 1])
    header_labels = ['Category', 'Sub-Category', 'Variable Name', 'Weight(%)']
    
    for i, label in enumerate(header_labels):
        with cols[i]:
            st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 2px'>{label}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 

    for i in range(0, len(ahp_weights)):
        cols = st.columns([2, 2, 2, 1])
        with cols[0]:
            st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_weights['Category'][i]}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_weights['Sub-category'][i]}</div>", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_weights['Variable Name'][i]}</div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{round(100*ahp_weights['Weight'][i], 1)}</div>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)

def view_model_report(model_id, prod_type):
    # st.write(' ')
    st.markdown("""
    <style>
    /* Flex container for tabs */

    /* Individual tabs */
    button[data-baseweb="tab"] {
        flex-grow: 1; /* Grow to fill space */
        text-align: center; /* Center text inside tabs */
    }
    .st-cr {
        color: black;
    }
    .st-d8 {
        color: black;
    }
    .main .block-container {
            max-width: 95%;
            # padding-left: 1%;
            # padding-right: 1%;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="border-radius: 5px;">
        <h2 style="text-align:left; color: black;">Product: {prod_type} - Model ID: {model_id}</h2>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(['Delphi Responses', 'AHP Responses', 'AHP Weights'])

    with tabs[0]:
        delphi_quest = pd.read_excel('Response.xlsx')
        users = pd.read_excel('Users.xlsx')
        delphi_quest = delphi_quest[delphi_quest['Model ID'] == model_id].reset_index(drop = True)
    
        delphi_quest = delphi_quest.merge(users[['email', 'f_name', 'l_name']], how = 'left', left_on = 'User', right_on = 'email').drop('email', axis = 1)
    
        delphi_quest['name_team'] = delphi_quest['f_name'].fillna('') + ' ' + delphi_quest['l_name'].fillna('') + ' (' + delphi_quest['Team'].fillna('') + '): ' + delphi_quest['Relevance'].fillna('')
    
        delphi_quest_relevance = delphi_quest.groupby(['Category', 'Sub-category', 'Variable Name']).apply(combine_relevance).reset_index(name='Combined Relevance')
        
        delphi_quest['Comment'] = delphi_quest['Comment'].fillna('')
        delphi_quest_comments = delphi_quest.loc[delphi_quest['Comment'] != '']
    
        delphi_quest_comments['Labeled Comments'] = delphi_quest_comments['f_name'].fillna('') + ' ' + delphi_quest_comments['l_name'].fillna('') + ' (' + delphi_quest_comments['Team'] + '): ' + delphi_quest_comments['Comment'].fillna('').str.lstrip()
    
        if len(delphi_quest_comments) > 0:
            delphi_quest_comments = delphi_quest_comments.groupby(['Category', 'Sub-category', 'Variable Name']).apply(combine_comments).reset_index(name='Combined Comments')
        else:
            delphi_quest_comments = pd.DataFrame(columns = ['Category', 'Sub-category', 'Variable Name', 'Combined Comments'])
    
        delphi_quest_df = delphi_quest_relevance.merge(delphi_quest_comments, how = 'left', on = ['Category', 'Sub-category', 'Variable Name'])
        delphi_quest_df['Combined Comments'] = delphi_quest_df['Combined Comments'].fillna(' ')
    
        delphi_ver = pd.read_excel('Delphi Verification Responses.xlsx')
        delphi_ver = delphi_ver[delphi_ver['Model ID'] == model_id].reset_index(drop = True)
        
        delphi_quest_df = delphi_quest_df.merge(delphi_ver[['Category', 'Sub-category', 'Variable Name', 'Your Comments', 'Relevance', 'Selected']], how = 'left', on = ['Category', 'Sub-category', 'Variable Name'])
        
        delphi_quest_df['Your Comments'] = np.where(delphi_quest_df['Your Comments'].isna(), 'NA', 'Delphi Reviewer: ' + delphi_quest_df['Your Comments'].astype(str))

        delphi_quest_df['Combined Comments'] = delphi_quest_df.apply(lambda row: f"{row['Combined Comments']}\n{row['Your Comments']}", axis=1)
        delphi_quest_df['Combined Comments'] = np.where(delphi_quest_df['Combined Comments'].isna(), 'NA', delphi_quest_df['Combined Comments'])
        delphi_quest_df['Combined Comments'] = delphi_quest_df['Combined Comments'].apply(lambda x: x.replace('Delphi Reviewer:', '\nDelphi Reviewer:').strip())

        st.markdown("""
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            margin-top: -20px;
            # margin-bottom: 40px;
            # padding-right: 10px;
            font-size: 14px;
        }
        .boldhr {
            width: 100%;
            height: 1.3px;
            background-color: #9c9b99; 
            margin: 2px;
            margin-top: -5px;
        }
        hr {
            margin-top: 0px;
            margin-bottom: 0px;
            background-color: #9c9b99; 
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
    
        cols = st.columns([0.7, 0.7, 0.85, 1, 1, 0.6, 0.6, 0.6])
        header_labels = ['Category', 'Sub-Category', 'Variable Name', 'Selected Relevances', 'Comments', 'Final Relevance', 'Engine Selection', 'Final Selection']
        
        for i, label in enumerate(header_labels):
            with cols[i]:
                st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 2px'>{label}</div>", unsafe_allow_html=True)
    
        st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
        
        variables = list(set(delphi_quest_df['Variable Name']))
        
        for i in range(0, len(delphi_quest_df)):
            cat = delphi_quest_df['Category'][i]
            sub_cat = delphi_quest_df['Sub-category'][i]
            var_name = delphi_quest_df['Variable Name'][i]
            relevance = delphi_quest_df['Combined Relevance'][i]
            comments = delphi_quest_df['Combined Comments'][i]
            selected_relevance = delphi_quest_df['Relevance'][i]
            selected_final = delphi_quest_df['Selected'][i]
    
            if (selected_relevance == 'Low'):
                selected_relevance_val = 'Excluded'
            else: 
                selected_relevance_val = 'Included'
    
            if (selected_final == False):
                selected_final_val = 'Excluded'
            else: 
                selected_final_val = 'Included'
            
            cols = st.columns([0.7, 0.7, 0.85, 1, 1, 0.6, 0.6, 0.6])
            with cols[0]:
                st.markdown(f"<div class='centered' style='padding: 4px; margin-top: -15px;'>{cat}</div>", unsafe_allow_html=True)
                
            with cols[1]:
                st.markdown(f"<div class='centered' style='padding: 4px; margin-top: -15px;'>{sub_cat}</div>", unsafe_allow_html=True)
            
            with cols[2]:
                st.markdown(f"<div class='centered' style='padding: 4px; margin-top: -15px;'>{var_name}</div>", unsafe_allow_html=True)
            
            with cols[3]:
    
                formatted_text = re.sub(
                    r'^(.+?:)\s*(.*)$',
                    r"<span style='font-size: 14px; font-weight: bold;'>\1</span> <span style='font-size: 14px; line-height: 1;'>\2</span>",
                    relevance, flags=re.M)
                
                st.markdown(f"<div style='line-height: 1; margin-top: -10px;'>{formatted_text}</div>", unsafe_allow_html=True)
    
            with cols[4]:
                if comments != 'NA':
                    formatted_text = re.sub(
                        r'^(.+?:)\s*(.*)$',
                        r"<span style='font-size: 14px; font-weight: bold;'>\1</span> <span style='font-size: 14px; line-height: 0;'>\2</span>",
                        comments, flags=re.M)
                    
                    st.markdown(f"<div style='font-size: 14px; line-height: 1; margin-top: -10px;'>{formatted_text}</div>", unsafe_allow_html=True)
    
                else:
                    st.markdown(f"<div style='font-size: 14px; line-height: 1; margin-top: -10px; text-align: center;'>{'NA'}</div>", unsafe_allow_html=True)
    
            with cols[5]:
                st.markdown(f"<div style='line-height: 1; margin-top: -10px; text-align: center;'>{selected_relevance}</div>", unsafe_allow_html=True)
                
            with cols[6]:
                if selected_relevance_val == 'Included':
                    st.markdown(f"""<div style='font-size: 14px; text-align: center; background-color: #CFF4D0; color: green; border-radius: 5px; margin-top: -10px;'>{selected_relevance_val}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style='font-size: 14px; text-align: center; background-color: #FFE7E7;color: #6E0202;border-radius: 5px; margin-top: -10px;'>{selected_relevance_val}</div>""", unsafe_allow_html=True)
                # st.write()
    
            with cols[7]:
                if selected_final_val == 'Included':
                    st.markdown(f"""<div style='font-size: 14px; text-align: center; background-color: #CFF4D0; color: green; border-radius: 5px; margin-top: -10px;'>{selected_final_val}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div style='font-size: 14px; text-align: center; background-color: #FFE7E7;color: #6E0202;border-radius: 5px; margin-top: -10px;'>{selected_final_val}</div>""", unsafe_allow_html=True)
    
            st.markdown("<hr>", unsafe_allow_html=True)

    with tabs[1]:
        ahp_selection = pd.read_excel('AHP Selection.xlsx')
        users = pd.read_excel('Users.xlsx')
        
        ahp_selection = ahp_selection[ahp_selection['Model ID'] ==  st.session_state.model_id].reset_index(drop = True)
        ahp_selection['Header'] = ahp_selection['Sub-category']
        ahp_selection.loc[ahp_selection['Sub-category'] == 'Variables', 'Header'] = ahp_selection['Category']

        ahp_selection = ahp_selection.merge(users[['email', 'f_name', 'l_name', 'team']],
                                            how = 'left', left_on = 'User', right_on = 'email').drop('email', axis = 1)

        ahp_selection['selection_name_team'] = ahp_selection['f_name'].fillna('') + ' ' + ahp_selection['l_name'].fillna('') + ' (' + ahp_selection['team'].fillna('') + '): ' + ahp_selection['Selection'].fillna('')

        ahp_selection['magnitude_name_team'] = ahp_selection['f_name'].fillna('') + ' ' + ahp_selection['l_name'].fillna('') + ' (' + ahp_selection['team'].fillna('') + '): ' + ahp_selection['Magnitude'].astype(str)

        ahp_selection_val = ahp_selection.groupby(['Header', 'Criteria 1', 'Criteria 2']).apply(combine_selection).reset_index(name='Combined Selection')
        ahp_selection_mag = ahp_selection.groupby(['Header', 'Criteria 1', 'Criteria 2']).apply(combine_magnitude).reset_index(name='Combined Magnitude')

        ahp_selection_df = ahp_selection_val.merge(ahp_selection_mag, how = 'left', on = ['Header', 'Criteria 1', 'Criteria 2'])
        
        # st.write(ahp_selection_df)

        tab_cols = st.columns([0.5, 5, 0.5])

        with tab_cols[1]:
            st.markdown("""
            <style>
            .centered {
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                margin-top: -20px;
                # margin-bottom: 40px;
                # padding-right: 10px;
                font-size: 14px;
            }
            .boldhr {
                width: 100%;
                height: 1.3px;
                background-color: #9c9b99; 
                margin: 2px;
                margin-top: -5px;
            }
            hr {
                margin-top: -6px;
                margin-bottom: 0px;
                background-color: white; 
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
        
            cols = st.columns([2, 2, 2, 2, 1.5])
            header_labels = ['Category', 'Criteria 1', 'Criteria 2', 'Selected Variable', 'Magnitude']
            
            for i, label in enumerate(header_labels):
                with cols[i]:
                    st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: 2px'>{label}</div>", unsafe_allow_html=True)
        
            st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 

            for i in range(0, len(ahp_selection_df)):
                cols = st.columns([2, 2, 2, 2, 1.5])
                with cols[0]:
                    st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_selection_df['Header'][i]}</div>", unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_selection_df['Criteria 1'][i]}</div>", unsafe_allow_html=True)
                with cols[2]:
                    st.markdown(f"<div class='centered' style='margin-bottom: 2px'>{ahp_selection_df['Criteria 2'][i]}</div>", unsafe_allow_html=True)
                with cols[3]:
                    formatted_text = re.sub(
                        r'^(.+?:)\s*(.*)$',
                        r"<span style='font-size: 14px; font-weight: bold;'>\1</span> <span style='font-size: 14px; line-height: 0;'>\2</span>",
                        ahp_selection_df['Combined Selection'][i], flags=re.M)
                    st.markdown(f"<div style='font-size: 14px; line-height: 1; margin-top: -10px;'>{formatted_text}</div>", unsafe_allow_html=True)
                with cols[4]:
                    formatted_text = re.sub(
                        r'^(.+?:)\s*(.*)$',
                        r"<span style='font-size: 14px; font-weight: bold;'>\1</span> <span style='font-size: 14px; line-height: 0;'>\2</span>",
                        ahp_selection_df['Combined Magnitude'][i], flags=re.M)
                    st.markdown(f"<div style='font-size: 14px; line-height: 1; margin-top: -10px;'>{formatted_text}</div>", unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)

    with tabs[2]:
        ahp_weights = pd.read_excel('Weights.xlsx', sheet_name = 'Weights Agg')
        ahp_weights = ahp_weights[ahp_weights['Model ID'] ==  st.session_state.model_id].reset_index(drop = True)

        tab_cols = st.columns([0.5, 5, 0.5])

        with tab_cols[1]:
            # Application Variables
            av_ahp_weights = ahp_weights[~ahp_weights['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])].reset_index(drop = True)
            model_report_ahp_weights('Application Variables', av_ahp_weights)
    
            # Behvioral Variables
            bv_ahp_weights = ahp_weights[ahp_weights['Category'].isin(['Behavioral Variables'])].reset_index(drop = True)
            model_report_ahp_weights('Behavioral Variables', bv_ahp_weights)
    
            # Adjustments / Downgrade Factors
            af_ahp_weights = ahp_weights[ahp_weights['Category'].isin(['Adjustments / Downgrade Factors'])].reset_index(drop = True)
            model_report_ahp_weights('Adjustments / Downgrade Factors', af_ahp_weights)
    
            # Early Warning Indicators
            ewi_ahp_weights = ahp_weights[ahp_weights['Category'].isin(['Early Warning Indicators'])].reset_index(drop = True)
            model_report_ahp_weights('Early Warning Indicators', ewi_ahp_weights)

    cols_button = st.columns(5)
    ChangeButtonColour('Home', 'black', '#b3c3d9', '20px')
    if cols_button[2].button('Home', key='back_view_report'):
        st.session_state.page = 'admin_models'
        st.session_state.need_rerun = True
        if st.session_state.need_rerun:
            st.session_state.need_rerun = False
            st.rerun()

def gen_new_model_text(text, df):
    st.markdown(f"""<ul style='list-style-type: disc;'><li style='margin-top: -15px; font-size: 14px;'>{text}</li></ul>""", unsafe_allow_html=True)

    for i in range(0, len(df)):
        st.markdown(f"""<ul style='list-style-type: circle;'><li style='margin-left: 45px; margin-top: -16px; font-size: 14px;'>{df['name'][i]} of {df['Team'][i]} team.</li></ul>""", unsafe_allow_html=True)

def under_dev_status_update(step, temp_df):
    
    st.markdown(f"""<div class='markdown-spacing' style='color: black; font-size: 14px;'>{step}</div>""", unsafe_allow_html=True)
    
    for i in range(0, len(temp_df)):
        
        if (temp_df['questionnaire'][i] == 'AHP') & (temp_df['completed'][i] == 1):
            st.markdown(f"""<div class='markdown-spacing' style='color: green;'><ul><li>AHP questionnaire has been submitted by {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)
        
        if (temp_df['questionnaire'][i] == 'AHP') & (temp_df['completed'][i] == 0):
            st.markdown(f"""<div class='markdown-spacing' style='color: #d63f3f;'><ul><li>AHP questionnaire pending from {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)

        if step == 'Step 1:':
            if (temp_df['questionnaire'][i] == 'Delphi') & (temp_df['completed'][i] == 1):
                st.markdown(f"""<div class='markdown-spacing' style='color: green;'><ul><li>Delphi questionnaire has been submitted by {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)
        
            if (temp_df['questionnaire'][i] == 'Delphi') & (temp_df['completed'][i] == 0):
                st.markdown(f"""<div class='markdown-spacing' style='color: #d63f3f;'><ul><li>Delphi questionnaire pending from {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)

        if step == 'Step 2:':
            if (temp_df['questionnaire'][i] == 'Delphi') & (temp_df['completed'][i] == 1) & (temp_df['reviewer'][i] == 'Yes') & (temp_df['reviewed'][i] == 1):
                st.markdown(f"""<div class='markdown-spacing' style='color: green;'><ul><li>Delphi verification has been submitted by {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)
    
            if (temp_df['questionnaire'][i] == 'Delphi') & (temp_df['reviewer'][i] == 'Yes') & (temp_df['reviewed'][i] == 0):
                st.markdown(f"""<div class='markdown-spacing' style='color: #d63f3f;'><ul><li>Delphi verification pending from {temp_df['u_name'][i]} of {temp_df['team'][i]} team.</li></ul></div>""", unsafe_allow_html=True)

        
        if (temp_df['questionnaire'][i] == 'Aggregation') & (temp_df['completed'][i] == 1):
            st.markdown(f"""<div class='markdown-spacing' style='color: green;'><ul><li>AHP weight(s) aggregation is done by Model Development Team.</li></ul></div>""", unsafe_allow_html=True)

        if (temp_df['questionnaire'][i] == 'Aggregation') & (temp_df['completed'][i] == 0):
            st.markdown(f"""<div class='markdown-spacing' style='color: #d63f3f;'><ul><li>AHP weight(s) aggregation is pending by Model Development Team.</li></ul></div>""", unsafe_allow_html=True)


        if (temp_df['questionnaire'][i] == 'Calibration') & (temp_df['completed'][i] == 1):
            st.markdown(f"""<div class='markdown-spacing' style='color: green;'><ul><li>AHP calibration is done by Model Development Team.</li></ul></div>""", unsafe_allow_html=True)

        if (temp_df['questionnaire'][i] == 'Calibration') & (temp_df['completed'][i] == 0):
            st.markdown(f"""<div class='markdown-spacing' style='color: #d63f3f;'><ul><li>Model calibration is pending by Model Development Team.</li></ul></div>""", unsafe_allow_html=True)

    st.write('')

def admin_models():
    # st.write(' ')
    st.markdown(f"""
    <div style="border-radius: 5px;">
        <h2 style="text-align:left; color: black; font-weight: bold;">Models</h2>
    </div>
    """, unsafe_allow_html=True)
    
    admin_sidebar()

    st.markdown("""
    <style>
    /* Flex container for tabs */

    /* Individual tabs */
    button[data-baseweb="tab"] {
        flex-grow: 1; /* Grow to fill space */
        text-align: center; /* Center text inside tabs */
    }
    .st-cr {
        color: black;
    }
    .st-d8 {
        color: black;
    }
    .main .block-container {
            max-width: 80%;
            # padding-left: 1%;
            # padding-right: 1%;
        }
    </style>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(['Generate New Model', 'Existing Models', 'Under Development', 'Finalise AHP Weights'])

    with tabs[0]:

        if 'prod' not in st.session_state:
            st.session_state['prod'] = None
        if 'reset_flag' not in st.session_state:
            st.session_state['reset_flag'] = False
            
        cols = st.columns([0.6, 2, 2, 0.6])

        with cols[1]:

            st.write('Select Product:')

        with cols[2]:
            st.markdown("""
                <style>
                    .stSelectbox {
                        margin-top: -48px;
                    }
                </style>
                """, unsafe_allow_html=True)

            if st.session_state['reset_flag']:
                st.session_state['prod'] = None
                st.session_state['reset_flag'] = False

            options = ['POS', 'CRE IPRE', 'MBBF IPRE', 'MBBF Business', 'Business Credit Card']
            initial_index = 0 if st.session_state['prod'] is None else options.index(st.session_state['prod'])
            prod_type = st.selectbox('', options = options, index = initial_index, key='prod')

        cols = st.columns([0.6, 4, 0.6])

        with cols[1]:
            roles_ex = pd.read_excel('Roles.xlsx')
            users = pd.read_excel('Users.xlsx')
    
            roles_ex = roles_ex.merge(users[['email', 'f_name', 'l_name']], how = 'left',
                                      left_on = 'Email ID', right_on = 'email').drop('email', axis = 1)
    
            roles_ex['name'] = roles_ex['f_name'].fillna('') + ' ' + roles_ex['l_name'].fillna('')
            
            ahp_users = roles_ex[(roles_ex['Product'] == prod_type) & (roles_ex['Questionnaire'] == 'AHP')].reset_index(drop = True)
            delphi_users = roles_ex[(roles_ex['Product'] == prod_type) & (roles_ex['Questionnaire'] == 'Delphi')].reset_index(drop = True)
            delphi_reviewer = roles_ex[(roles_ex['Product'] == prod_type) & (roles_ex['Questionnaire'] == 'Delphi') & (roles_ex['Reviewer'] == 'Yes')].reset_index(drop = True)
    
            errors = []
            if (len(ahp_users) == 0):
                errors.append('Assign user(s) for AHP questionnaire to generate new model.')
            
            if (len(delphi_users) == 0):
                errors.append('Assign user(s) for Delphi questionnaire to generate new model.')
            
            if (len(delphi_reviewer) == 0):
                errors.append('Assign a user for verification of Delphi questionnaire to generate new model.')
                
            cols = st.columns([0.3, 4, 0.3])
    
            with cols[1]:
                if (len(errors) != 0)  and (prod_type != None):
                    st.markdown(f"""<div style='background-color: #FFE7E7; color: #6E0202; padding-left: 10px; border-radius: 0px; padding-bottom: 5px;'><p>{'Resolve the following error(s):'}</p></div>""", unsafe_allow_html=True)
                    for i in range(0, len(errors)):
                        st.markdown(f"""<div style='background-color: #FFE7E7; color: #6E0202; padding-left: 10px; border-radius: 0px; margin-top: -17px;'><p>{i+1}. {errors[i]}</p></div>""", unsafe_allow_html=True)
                        
            if len(errors) == 0:
                gen_new_model_text('Response(s) for Delphi questionnaire will be requested from:', delphi_users)
                st.write(' ')
                gen_new_model_text('Response for Delphi verification will be requested from:', delphi_reviewer)
                st.write(' ')
                gen_new_model_text('Response(s) for AHP questionnaire will be requested from:', ahp_users)

        if (len(errors) == 0) and (prod_type != None):
            disable_button = False
        else:
            disable_button = True
            
        cols = st.columns([1.5, 1, 1.5])
        ChangeButtonColour('Request Responses', 'black', '#b3c3d9', '20px', disable_button)
        if cols[1].button('Request Responses', key=f'request_response', disabled = disable_button):
            st.session_state['reset_flag'] = True

            df_cols = ['model_id', 'product', 'team', 'user', 'questionnaire',	'reviewer',	'completed', 'reviewed', 'step']
            assign_forms_ex = pd.read_excel('assign_forms.xlsx')
            model_id = 1 if np.isnan(assign_forms_ex['model_id'].max()) else assign_forms_ex['model_id'].max() + 1

            temp_df = roles_ex[roles_ex['Product'] == prod_type][['Product', 'Team', 'Email ID', 'Questionnaire', 'Reviewer']]
            temp_df['completed'] = 0
            temp_df['reviewed'] = 0
            temp_df['step'] = 1
            temp_df.insert(0, 'model_id', model_id)
            temp_df.columns = df_cols

            temp_df.loc[temp_df['questionnaire'] == 'AHP', 'step'] = 2
            
            ahp_agg_list = [model_id, prod_type, 'Admin', 'Admin', 'Aggregation', 'No', 0, 0, 3]
            ahp_agg_df = pd.DataFrame(ahp_agg_list).T
            ahp_agg_df.columns = df_cols

            # model_calbration_list = [model_id, prod_type, 'Admin', 'Admin', 'Calibration', 'No', 0, 0, 4]
            # model_calbration_df = pd.DataFrame(model_calbration_list).T
            # model_calbration_df.columns = df_cols

            assign_forms_ex = pd.concat([assign_forms_ex, temp_df, ahp_agg_df]).reset_index(drop = True)
            # assign_forms_ex.to_excel('assign_forms.xlsx', index=False)
            with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                assign_forms_ex.to_excel(writer, sheet_name='Sheet1', index=False)

            cols = st.columns([0.3, 4, 0.3])
            with cols[1]:
                show_prompt_for_seconds(3, 'The responses has been requested successfully.')

            st.session_state.need_rerun = True
            if st.session_state.need_rerun:
                st.session_state.need_rerun = False
                st.rerun()
    
    with tabs[1]:
        assigned_forms =  pd.read_excel('assign_forms.xlsx')
        model_state =  pd.read_excel('assign_forms.xlsx', sheet_name = 'model_state')
        products_list = list(set(assigned_forms['product']))
        # st.write(assigned_forms)

        completed_count = 0
        
        for prod in products_list:
            temp_prod_df = model_state[(model_state['product'] == prod)].reset_index(drop = True)
            agg_completed_models = list(set(assigned_forms[(assigned_forms['product'] == prod) & (assigned_forms['questionnaire'] == 'Aggregation') & (assigned_forms['completed'] == 1)]['model_id']))

            if len(agg_completed_models) >0 :
                completed_count += 1
                
                with st.expander(prod):   

                    st.markdown("""
                    <style>
                    .centered {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        margin-top: -30px;
                        margin-bottom: 40px;
                        # padding-right: 10px;
                        font-size: 14px;
                        height: 10px;
                    }
                    .boldhr {
                        width: 100%;
                        height: 1px;
                        background-color: #9c9b99; 
                        # margin: 2px;
                        margin-top: -20px;
                    }
                    .popover_button {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        font-size: 14px;
                    }
                    .st-emotion-cache-12w0qpk {
                        width: calc(25% - 1rem);
                        flex: 1 1 calc(25% - 1rem);
                        height: 10px; /* Specify the desired height here */
                    }

                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 

                    cols = st.columns(4)
                    
                    header_labels = ['Model ID', 'Developed At', 'Model Report', 'Status']
                    
                    for i, label in enumerate(header_labels):
                        with cols[i]:
                            st.markdown(f"<div class='centered' style='font-weight: bold; margin-bottom: -10px'>{label}</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True) 
                    
                    for i in range(0, len(temp_prod_df)):
                        # st.write(temp_prod_df)
                        cols = st.columns(4)
                        with cols[0]:
                            st.markdown(f"<div class='centered' style='margin-bottom: -10px'>{temp_prod_df['model_id'][i]}</div>", unsafe_allow_html=True)
                        with cols[1]:
                            st.markdown(f"<div class='centered' style='margin-bottom: -10px'>{str(temp_prod_df['added_at'][i]).split('.')[0]}</div>", unsafe_allow_html=True)
                        with cols[2]:
                            # st.markdown(f"<div class='centered'>{'View'}</div>", unsafe_allow_html=True)
                            col_view_report = st.columns(1)
                            ChangeButtonColour('View Report', '#4088e6', 'transparent', '5px', False, '-45px', '-10px', '0px', 'center', 'underline', '0px', '0px', '0px', '0px', border = 'None')
                            if col_view_report[0].button('View Report', key=f'{i}_{temp_prod_df['model_id'][i]}_view_report'):

                                st.session_state.model_id = temp_prod_df['model_id'][i]
                                st.session_state.prod_type = temp_prod_df['product'][i]

                                st.session_state.page = 'view_model_report'
                                st.session_state.need_rerun = True
                                if st.session_state.need_rerun:
                                    st.session_state.need_rerun = False
                                    st.rerun() 

                        # with cols[3]:
                        #     # st.markdown(f"<div class='centered' style='height: 1px;'>{'Calibration'}</div>", unsafe_allow_html=True)
                        #     cols_delete = st.columns(1)
                        #     ChangeButtonColour('Calibrate', '#4088e6', 'transparent', '5px', False, '-45px', '0px', '0px', 'center', 'underline', '0px', '0px', '0px', '0px', border = 'None')
                        #     if cols_delete[0].button('Calibrate', key=f'{i}_{temp_prod_df['model_id'][i]}_calibration'):

                        #         st.session_state.model_id = temp_prod_df['model_id'][i]
                        #         st.session_state.prod_type = temp_prod_df['product'][i]

                        #         st.session_state.page = 'calibrate_model'
                        #         st.session_state.need_rerun = True
                        #         if st.session_state.need_rerun:
                        #             st.session_state.need_rerun = False
                        #             st.rerun() 

                                
                                    
                        with cols[3]:

                            if temp_prod_df['active'][i] == 0:

                                st.markdown("""
                                <style>
                                .stPopoverBody {
                                margin: 0px;
                                padding: 0px;
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
                                            # margin-bottom: -300px;
                                            margin-top: -60px;
                                            margin-left: 55px;
                                            border: none;
                                            color: #4088e6;
                                            font-size: 14px;
                                            text-decoration: underline;
                                            background-color: transparent;
                                        }
                                        """,
                                ):
                                
                                    with st.popover("Deploy"):
                                        st.markdown(f"<div class='popover_button'>Are you sure you want to deploy?</div>", unsafe_allow_html=True)
                                        # st.button('Yes', key = i)
                                        cols_delete = st.columns(3)
                                        ChangeButtonColour('Yes', 'black', '#b3c3d9', '5px', False, '10px', '-30px', '0px')
        
                                        if cols_delete[1].button('Yes', key=f'{i}_{temp_prod_df['model_id'][i]}_delete'):
    
                                            model_state = pd.read_excel('assign_forms.xlsx', sheet_name = 'model_state')
                                            
                                            model_state.loc[((model_state['product'] == temp_prod_df['product'][i])), 'active'] = 0
    
                                            model_state.loc[((model_state['model_id'] == temp_prod_df['model_id'][i]) &
                                                             (model_state['product'] == temp_prod_df['product'][i])), 'active'] = 1
    
                                            with pd.ExcelWriter('assign_forms.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                                model_state.to_excel(writer, sheet_name='model_state', index=False)
    
                                            weights_agg = pd.read_excel('Weights.xlsx', sheet_name = 'Weights Agg')
    
                                            weights_agg.loc[((weights_agg['Product'] == temp_prod_df['product'][i])), 'Active'] = 0
    
                                            weights_agg.loc[((weights_agg['Model ID'] == temp_prod_df['model_id'][i]) &
                                                             (weights_agg['Product'] == temp_prod_df['product'][i])), 'Active'] = 1
                                            with pd.ExcelWriter('Weights.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                                                weights_agg.to_excel(writer, sheet_name='Weights Agg', index=False)
                                                
                                            st.session_state.need_rerun = True
                                            if st.session_state.need_rerun:
                                                st.session_state.need_rerun = False
                                                st.rerun()
                            
                            else:
                                state = 'Currently Deployed'
                                st.markdown(f"<div class='centered' style='margin-top: -25px; margin-botton: -50px;'>{state}</div>", unsafe_allow_html=True)
        
        if completed_count == 0:
            st.markdown(f"<div style='justifyContent: center;'><i>No model has been pushed to production.</i></div>", unsafe_allow_html=True)
    
    
    
    with tabs[2]:

        st.markdown("""
        <style>
        .markdown-spacing {
            margin-top: -5px;  /* Reduce the top margin */
            margin-bottom: -30px;  /* Reduce the bottom margin */
        }
        </style>
        """, unsafe_allow_html=True)

        cols = st.columns(9)
        with cols[0]:
            st.markdown(f"<div style='justifyContent: left; font-size: 14px; margin-top: -1px; margin-bottom: 30px; color: #E81224;'>🟥 Pending</div>", unsafe_allow_html=True)

        with cols[1]:
            st.markdown(f"<div style='justifyContent: left; font-size: 14px; margin-top: -1px; margin-bottom: 30px; margin-left: -20px; color: green;'>🟩 Submitted</div>", unsafe_allow_html=True)
        
        under_dev = pd.read_excel('assign_forms.xlsx')
        users = pd.read_excel('Users.xlsx')
        under_dev = under_dev.merge(users[['email', 'f_name', 'l_name']], how = 'left', left_on = 'user', right_on = 'email').drop('user', axis = 1)
        under_dev['u_name'] = under_dev['f_name'].fillna('') + ' ' + under_dev['l_name'].fillna('')

        if len(under_dev) == 0:
            st.write('No models have been developed yet.')
        
        for model_id in list(set(under_dev['model_id'])):
            temp_df = under_dev[under_dev['model_id'] == model_id].sort_values(['step', 'questionnaire', 'reviewer'], ascending=[True, False, True]).reset_index(drop = True)
            temp_df['act_count'] = 1
            temp_df.loc[(temp_df['questionnaire'] == 'Delphi') & (temp_df['reviewer'] == 'Yes'), 'act_count'] = 2
            
            temp_df['done_count'] = temp_df['completed']
            temp_df.loc[(temp_df['questionnaire'] == 'Delphi') & (temp_df['reviewer'] == 'Yes') & (temp_df['reviewed'] == 1), 'done_count'] = 2

            grouped_temp_df = temp_df.groupby(['model_id']).agg(done_count = ('done_count', 'sum'), act_count = ('act_count', 'sum')).reset_index(drop = True)
            
            if grouped_temp_df['act_count'][0] > grouped_temp_df['done_count'][0]:
                
                completed_count = round(100*grouped_temp_df['done_count']/grouped_temp_df['act_count'], 0)
                with st.expander(f'Model ID: {model_id} - {temp_df['product'][0]} ({str(completed_count[0]).split('.')[0]}%)'):
                    
                    under_dev_status_update('Step 1:', temp_df[(temp_df['questionnaire'] == 'Delphi')].reset_index(drop = True))
                    under_dev_status_update('Step 2:', temp_df[(temp_df['questionnaire'] == 'Delphi') & (temp_df['reviewer'] == 'Yes')].reset_index(drop = True))
                    under_dev_status_update('Step 3:', temp_df[(temp_df['questionnaire'] == 'AHP')].reset_index(drop = True))
                    under_dev_status_update('Step 4:', temp_df[(temp_df['questionnaire'] == 'Aggregation')].reset_index(drop = True))
                    # under_dev_status_update('Step 5:', temp_df[(temp_df['questionnaire'] == 'Calibration')].reset_index(drop = True))

    with tabs[3]:

        assigned_forms = pd.read_excel('assign_forms.xlsx')
        ahp_agg_df = assigned_forms[(assigned_forms['questionnaire'] == 'Aggregation') & (assigned_forms['completed'] == 0)].reset_index(drop = True)

        models_list = list(set(ahp_agg_df['model_id']))
        
        row_num = 0
        for model_id in models_list:
            if len(assigned_forms[(assigned_forms['model_id'] == model_id) & (assigned_forms['questionnaire'] == 'AHP') & (assigned_forms['completed'] == 0)]) == 0:
                
                temp_df = ahp_agg_df[ahp_agg_df['model_id'] == model_id].reset_index(drop = True)
                
                ChangeButtonColour(f'{row_num+1}._{temp_df['product'][0]}-{temp_df['questionnaire'][0]}-{temp_df['model_id'][0]}', 'black', 'transparent', '0px', False, f'{-40}px', '0px', '0px', 'left', 'underline', border = 'None')
                if st.button(f'{row_num+1}._{temp_df['product'][0]}-{temp_df['questionnaire'][0]}-{temp_df['model_id'][0]}', key = f'{temp_df['model_id'][0]}_{temp_df['product'][0]}_ahp'):
                    
                    st.session_state.model_id = model_id
                    st.session_state.product = temp_df['product'][0]

                    st.session_state.page = 'ahp_weights_agg'
                    st.session_state.need_rerun = True
                    if st.session_state.need_rerun:
                        st.session_state.need_rerun = False
                        st.rerun()

                row_num += 1

        if row_num == 0:
            st.markdown(f"<div style='justifyContent: center;'><i>No pending models for AHP aggregation.</i></div>", unsafe_allow_html=True)

    # with tabs[4]:
    #     st.write(1)


def calibrate_model():
    
    css = """
    <style>
    .main .block-container {
        max-width: 50%;
        padding-left: 1%;
        padding-right: 1%;
    }
    .stNumberInput {
            margin-top: -30px;  /* Adjust the negative margin as needed */
    }
    .boldhr {
        width: 100%;
        height: 1px;
        background-color: #9c9b99; 
    }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)
    cols = st.columns([0.02, 2.55])
    with cols[1]:
        st.markdown(f"""<div style="border-radius: 5px;"><h3 style="text-align:left; color: black; font-weight: bold;">Calibration for Model ID {st.session_state.model_id} of Product {st.session_state.prod_type}</h3></div>""", unsafe_allow_html=True)

    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)

    cols = st.columns([0.05, 1.5, 1, 0.05])
    with cols[1]:
        st.write('Enter the central tendancy for Application Variables.')

    with cols[2]:
        av_val = st.number_input(label = '', key = 'av_ct')

    cols = st.columns([0.05, 1.5, 1, 0.05])
    with cols[1]:
        st.write('Enter the central tendancy for Behavioral Variables.')

    with cols[2]:
        bv_val = st.number_input(label = '', key = 'bv_ct')




    



    # import numpy as np
    # from scipy.optimize import minimize
    
    # # Objective function to minimize the square of the difference
    # def objective_function(params):
    #     alpha, beta = params
    #     return (alpha + beta - 0.0394) ** 2
    
    # # Initial guess
    # initial_guess = [0, 1]
    
    # # Set optimization method to BFGS which is a good general-purpose optimizer
    # result = minimize(objective_function, initial_guess, method='BFGS')
    
    # # Optimized alpha and beta
    # optimized_alpha, optimized_beta = result.x
    
    # # Print the results
    # st.write("Optimized Alpha:", optimized_alpha)
    # st.write("Optimized Beta:", optimized_beta)


    import numpy as np
    from scipy.optimize import minimize
    import tkinter as tk
    from tkinter import simpledialog
    
    # Define the optimization function (example: quadratic function)
    def objective_function(x):
        return x[0]**2 + x[1]**2
    
    # Create the GUI
    root = tk.Tk()
    root.geometry("400x300")
    
    # Inputs for the objective function and variables
    objective_var = simpledialog.askstring("Input", "Enter the objective cell (e.g., 'x**2 + y**2')", parent=root)
    variables = simpledialog.askstring("Input", "Enter the variable names separated by comma (e.g., 'x, y')", parent=root)
    
    # Parse the variables
    variables = variables.split(',')
    
    # Initial guesses
    initial_guesses = np.zeros(len(variables))
    
    # Constraints (could be more interactive and complex in a full application)
    cons = ({'type': 'eq', 'fun': lambda x: np.array([x[0] + x[1] - 1])})
    
    # Perform the optimization
    result = minimize(objective_function, initial_guesses, method='SLSQP', constraints=cons)
    
    # Show the results
    result_label = tk.Label(root, text=f"Optimal values: {result.x}\nMinimum value: {result.fun}")
    result_label.pack()
    
    root.mainloop()

    cols_button = st.columns(3)
    ChangeButtonColour('Back', 'black', '#b3c3d9', '20px', margin_top = '50px')
    if cols_button[1].button('Back', key='back_calibrate_models'):
        st.session_state['page'] = 'admin_models'
        st.session_state.need_rerun = True
        st.session_state.need_rerun = False
        st.rerun()



def user_sidebar():

    with st.sidebar:
        cols = st.columns([0.3, 4, 0.3])

        with cols[1]:
            css = """
            <style>
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #b3c3d9;  /* Change this color to any hex color you prefer */
            }
            </style>
            """
        
            st.markdown(css, unsafe_allow_html=True)
            st.write(f'Logged in as: \n{st.session_state.user_name}')
    
            # st.markdown("""
            # <style>
            # div.stButton > button:first-child {
            #     background-color: #b3c3d9; /* Change background to blue */
            #     color: black; /* Change text color to white */
            #     border: none;
            #     margin-bottom: -50px;
            #     # text-decoration: underline; /* Add underline to the text */
                
            # }
            # /* Add CSS for centering the button */
            # div.stButton {
            #     display: flex;
            #     justify-content: center; /* Align button horizontally center */
            # }
            # hr {
            #     margin-bottom: 0px;
            #     background-color: #9c9b99; 
            # }
            # </style>
            # """, unsafe_allow_html=True)


        cols = st.columns([1, 8, 1])
        ChangeButtonColour('Logout', 'black', '#b3c3d9', '20px')
        if cols[1].button('Logout', key='admin_logout'):
        # if st.button('Logout'):
            st.session_state.page = 'login'
            st.session_state.need_rerun = True
            if st.session_state.need_rerun:
                st.session_state.need_rerun = False
                st.rerun()
            
            # st.markdown("<hr>", unsafe_allow_html=True)
            # # st.button('Responses')
            # # st.markdown("<hr>", unsafe_allow_html=True)
            # # st.button('Completed')
            # # st.markdown("<hr>", unsafe_allow_html=True)
        
            # if st.button('Logout'):
            #     st.session_state.page = 'login'
            #     st.session_state.need_rerun = True
            #     if st.session_state.need_rerun:
            #         st.session_state.need_rerun = False
            #         st.rerun()
                    
            # st.markdown("<hr>", unsafe_allow_html=True)


def pending_page_users():

    st.markdown(f"""
    <div style="border-radius: 5px;">
        <h2 style="text-align:left; color: black; font-weight: bold;">Responses</h2>
    </div>
    """, unsafe_allow_html=True)
    
    user_sidebar()

    roles = pd.read_excel('Roles.xlsx')
    assigned_forms = pd.read_excel('assign_forms.xlsx')

    temp_roles = roles[roles['Email ID'] == st.session_state.email].reset_index(drop = True)
    temp_quest = temp_roles[['Questionnaire', 'Reviewer']].drop_duplicates().reset_index(drop = True)
    temp_quest['tabs'] = temp_quest['Questionnaire'] + '-' + temp_quest['Reviewer']

    temp_assigned = assigned_forms[assigned_forms['user'] == st.session_state.email].reset_index(drop = True)

    # st.write(temp_assigned)

    role_tabs = []
    for i in range(0, len(temp_quest)):
        if temp_quest['tabs'][i] == 'AHP-No':
            role_tabs.append('AHP Questionnaire')
        elif temp_quest['tabs'][i] == 'Delphi-No':
            role_tabs.append('Delphi Questionnaire')
        else:
            role_tabs.append('Delphi Questionnaire')
            role_tabs.append('Delphi Verification')
    sorted_role_tabs = sorted(set(role_tabs))
    # st.write(sorted_role_tabs)

    for i in range(0, len(sorted_role_tabs)):
        if sorted_role_tabs[i] == 'AHP Questionnaire':

            custom_css = """
            <style>
                details {
                    # background-color: #b3c3d9; /* Light grey background */
                    background-color: white; /* Light grey background */
                    border: 2px solid #4a4e69; /* Dark grey border */
                    padding: 10px;
                    border-radius: 10px; /* Rounded corners */
                    margin: 10px 0;
                }
                summary {
                    font-weight: bold;
                }
            </style>
            """
            st.markdown(custom_css, unsafe_allow_html=True)

                
            with st.expander('AHP Questionnaire(s)', expanded=True):

                models_ahp = (assigned_forms[(assigned_forms['questionnaire'] == 'Delphi')].reset_index(drop = True))

                models_ahp_grouped = models_ahp.groupby(['model_id', 'product']).agg(count = ('model_id', 'count'),
                                                                             completed = ('completed', 'sum'),
                                                                             reviewed = ('reviewed', 'sum')).reset_index()

                models_ahp_list = list(set(models_ahp_grouped[models_ahp_grouped['count'] == models_ahp_grouped['reviewed']]['model_id']))

                ahp_q_df = assigned_forms[(assigned_forms['model_id'].isin(models_ahp_list)) & (assigned_forms['questionnaire'] == 'AHP') & (assigned_forms['user'] == st.session_state.email) & (assigned_forms['completed'] == 0)].reset_index(drop = True)

                if len(ahp_q_df) == 0:
                    st.markdown(f"<div style='justifyContent: center;'><i>No pending questionnaire(s).</i></div>", unsafe_allow_html=True)
                
                for j in range(0, len(ahp_q_df)):

                    ChangeButtonColour(f'{j+1}._{ahp_q_df['product'][j]}-{ahp_q_df['questionnaire'][j]}-{ahp_q_df['model_id'][j]}', 'black', 'transparent', '20px', False, f'{-40}px', '0px', '0px', 'left', 'underline', border = 'None')
                    if st.button(f'{j+1}._{ahp_q_df['product'][j]}-{ahp_q_df['questionnaire'][j]}-{ahp_q_df['model_id'][j]}', key = f'{ahp_q_df['model_id'][j]}_{ahp_q_df['product'][j]}_ahp'):

                        st.session_state['team'] = ahp_q_df['team'][j]
                        st.session_state['product'] = ahp_q_df['product'][j]
                        st.session_state['model_id'] = ahp_q_df['model_id'][j]
                        vars_all = pd.read_excel('Delphi Verification Responses.xlsx')
                        st.session_state['shortlisted_vars'] = vars_all.loc[(vars_all['Selected'] == True) & (vars_all['Model ID'] == st.session_state['model_id'])].reset_index(drop = True)
                        

                        st.session_state.page = 'ahp_questionnaire_description'
                        st.session_state.need_rerun = True
                        if st.session_state.need_rerun:
                            st.session_state.need_rerun = False
                            st.rerun()
        
    
        elif sorted_role_tabs[i] == 'Delphi Questionnaire':
            with st.expander('Delphi Questionnaire(s)', expanded=True):
                
                delphi_q_df = temp_assigned[(temp_assigned['questionnaire'] == 'Delphi') & (temp_assigned['reviewed'] == 0) & (temp_assigned['completed'] == 0) ].reset_index(drop = True)
                
                if len(delphi_q_df) == 0:
                    st.markdown(f"<div style='justifyContent: center;'><i>No pending questionnaire(s).</i></div>", unsafe_allow_html=True)
                else:
                    for j in range(0, len(delphi_q_df)):
                        # -40 - j*20
                        ChangeButtonColour(f'{j+1}._{delphi_q_df['product'][j]}-{delphi_q_df['questionnaire'][j]}-{delphi_q_df['model_id'][j]}', 'black', 'transparent', '20px', False, f'{-40}px', '0px', '0px', 'left', 'underline', border = 'None')
                        if st.button(f'{j+1}._{delphi_q_df['product'][j]}-{delphi_q_df['questionnaire'][j]}-{delphi_q_df['model_id'][j]}', key = f'{delphi_q_df['model_id'][j]}_{delphi_q_df['product'][j]}_bt'):
                            
                            st.session_state['team'] = delphi_q_df['team'][j]
                            st.session_state['product'] = delphi_q_df['product'][j]
                            st.session_state['model_id'] = delphi_q_df['model_id'][j]

                            st.session_state.page = 'delphi_p1'
                            st.session_state.need_rerun = True
                            if st.session_state.need_rerun:
                                st.session_state.need_rerun = False
                                st.rerun()

        else:
            with st.expander('Delphi Verification(s)', expanded=True):
                
                models_ver = list(assigned_forms[(assigned_forms['reviewer'] == 'Yes') & (assigned_forms['reviewed'] == 0) & (assigned_forms['completed'] == 1) & (assigned_forms['user'] == st.session_state.email)]['model_id'])

                ver_models_list = []
                row_num = 0
                for model in models_ver:
                    delphi_v_df = assigned_forms[(assigned_forms['model_id'] == model) & (assigned_forms['questionnaire'] == 'Delphi')].reset_index(drop = True)
                    if len(delphi_v_df[delphi_v_df['completed'] == 0]) == 0:
                        ChangeButtonColour(f'{row_num+1}._{pd.unique(delphi_v_df['product'])[0]}-{pd.unique(delphi_v_df['questionnaire'])[0]} Verification-{pd.unique(delphi_v_df['model_id'])[0]}', 'black', 'transparent', '20px', False, f'{-40}px', '0px', '0px', 'left', 'underline', border = 'None')
                        
                        if st.button(f'{row_num+1}._{pd.unique(delphi_v_df['product'])[0]}-{pd.unique(delphi_v_df['questionnaire'])[0]} Verification-{pd.unique(delphi_v_df['model_id'])[0]}', key = f'{pd.unique(delphi_v_df['model_id'])[0]}_{pd.unique(delphi_v_df['product'])[0]}_ver'):
                            
                            st.session_state['delphi_ver_model'] = model 
                            st.session_state['product'] = pd.unique(delphi_v_df['product'])[0]
                            st.session_state['model_id'] = model
    
                            st.session_state.page = 'delphi_ver'
                            st.session_state.need_rerun = True
                            if st.session_state.need_rerun:
                                st.session_state.need_rerun = False
                                st.rerun()
                    
                        row_num += 1

                if row_num == 0:
                    st.markdown(f"<div style='justifyContent: center;'><i>No pending verification(s).</i></div>", unsafe_allow_html=True)


def gen_details():
    gen_vars = {}
    gen_vars['Customer Output'] = {}
    gen_vars['Generic Details'] = {}
    
    st.markdown("""
        <style>.small-font {
            font-size:25px !important;
            # font-weight: bold;
            margin-bottom: 0px;
        }
        .boldhr {
            width: 100%;
            height: 2px;
            background-color: #9c9b99; 
            # margin: 2px;
            # margin-top: -30px;
        }
        </style>
        """, unsafe_allow_html=True)

    # cols = st.columns(6)
    # with cols[0]:
    st.markdown(f'<p class="small-font">Generic Details</p>', unsafe_allow_html=True)

    # with cols[5]: 
    #     # st.write()
    #     st.markdown(f"<div style='margin-top: -70px'>{f'Logged in as:'}</div>", unsafe_allow_html=True)
    #     st.markdown(f"<div style='margin-top: -60px'>{st.session_state.user_name}</div>", unsafe_allow_html=True)
    #     cols_delete = st.columns(1)
    #     ChangeButtonColour('Logout', 'black', '#b3c3d9', '5px', False, '-40px', '-60px', '0px')
    #     if cols_delete[0].button('Logout', key=f'cr_logout_{st.session_state.email}'):
    #         st.session_state.page = 'login'
    #         st.session_state.need_rerun = True
    #         if st.session_state.need_rerun:
    #             st.session_state.need_rerun = False
    #             st.rerun()
                
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)

    gen_det_cols = ['Customer ID', 'Sector', 'Product', 'Audited Financial Statements Provided', 'Existing/New Borrower', 'Loan Extension', 'Recent Annual Review', 'Months Since Inception']

    temp_det_cols = gen_det_cols.copy()

    for i in range(0, int(len(gen_det_cols)/2)):
        
        cols = st.columns([0.2, 3, 2, 3, 2, 0.2])
        with cols[1]:
            st.write(f'{temp_det_cols[0]}:')
            
        with cols[2]:
            st.markdown("""
            <style>
            .stSelectbox {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            .stTextInput {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            </style>
            """, unsafe_allow_html=True)

            if temp_det_cols[0] == 'Customer ID':
                cust_id = st.text_input('', placeholder='Enter ID', key = 'cust_id_cr')
                gen_vars['Generic Details'][temp_det_cols[0]] = cust_id
            elif temp_det_cols[0] == 'Product':
                prod_type = st.selectbox(label = '', placeholder = 'Select Product', options = ['POS', 'CRE IPRE', 'MBBF IPRE', 'MBBF Business', 'Business Credit Card'], index = None, key = 'prod_type_cr')
                gen_vars['Generic Details'][temp_det_cols[0]] = prod_type
            elif temp_det_cols[0] == 'Existing/New Borrower':
                borrower_type = st.selectbox(label = '', options = ['Existing', 'New'], index = 0, key = f'{i}_1')
                gen_vars['Generic Details'][temp_det_cols[0]] = borrower_type
            else:
                annual_review = st.selectbox(label = '', options = ['Yes', 'No'], key = f'{i}_1')
                gen_vars['Generic Details'][temp_det_cols[0]] = annual_review

            temp_det_cols.remove(temp_det_cols[0])
            
    
        with cols[3]:
            st.write(f'{temp_det_cols[0]}:')
            
        with cols[4]:
            st.markdown("""
            <style>
            .stSelectbox {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            .stTextInput {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            .stNumberInput {
                    margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            </style>
            """, unsafe_allow_html=True)
            
            if temp_det_cols[0] == 'Sector':
                sector = st.selectbox(label = '', options = ['General', 'Manufacturing', 'Trading', 'Services'], index = 0, key = f'{i}_2')
                gen_vars['Generic Details'][temp_det_cols[0]] = sector
            elif temp_det_cols[0] == 'Audited Financial Statements Provided':
                afs = st.selectbox(label = '', options = ['AFS Provided', 'AFS Not Provided'], index = 0, key = f'{i}_2')
                gen_vars['Generic Details'][temp_det_cols[0]] = afs
            elif temp_det_cols[0] == 'Loan Extension':
                loan_ext = st.selectbox(label = '', options = ['Yes', 'No'], index = 0, key = f'{i}_2')
                gen_vars['Generic Details'][temp_det_cols[0]] = loan_ext
            else:                
                months = st.number_input(label = '', min_value = 0, key = f'{i}_2')
                gen_vars['Generic Details'][temp_det_cols[0]] = months
                
            temp_det_cols.remove(temp_det_cols[0])

    if ((borrower_type == 'Existing') and (annual_review == 'Yes')) or ((borrower_type == 'Existing') and (loan_ext == 'Yes')):
        av_bv_weight_type = 'Months Since Review'
    else:
        av_bv_weight_type = 'Months Since Inception'
        
    av_bv_weights_fin = st.session_state.av_bv_weight[(st.session_state.av_bv_weight['Type'] == av_bv_weight_type) & (st.session_state.av_bv_weight['Months'] == months)].reset_index(drop = True)[['BV', 'AV']]

    return av_bv_weights_fin, gen_vars #prod_type, cust_id#, borrower_type, annual_review, sector, afs, loan_ext, months



def get_rating_mrs(pd):
    mrs = st.session_state.mrs
    return mrs[(pd >= mrs['Low']) & (pd < mrs['High'])]['Rating'].iloc[0]


def max_step(temp_range):
    return max(temp_range[['Lower', 'Upper']].apply(lambda col: col.apply(lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0).max()))

def adj_factors(weights_af, adj_df, gen_vars):

    notch_cal, gen_vars = calculate_notches(weights_af, adj_df, 'Application Module Adjustment Factors', gen_vars)
    gen_vars['Application Module Adjustment Factors']['Notches'] = notch_cal
    
    cols = st.columns([0.2, 10, 0.2])
    with cols[1]:
        if st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] == True:

            mrs = st.session_state.mrs
            current_rating_index = mrs.index[mrs['Rating'] == st.session_state['overall_rating_av']][0]
            new_rating_index = int(max(int(min(current_rating_index-notch_cal, len(mrs) - 1)), 0))
            
            if new_rating_index != current_rating_index:
                st.session_state['adj_pd_av'] = mrs[new_rating_index:new_rating_index+1]['Mid'].iloc[0]
                st.session_state['adj_rating_av'] = mrs[new_rating_index:new_rating_index+1]['Rating'].iloc[0]
            
            else:
                st.session_state['adj_pd_av'] = st.session_state['overall_pd_av']
                st.session_state['adj_rating_av'] = st.session_state['overall_rating_av']

            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Notch Adjustment: <strong>{int(notch_cal)}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Application Module PD (Post Adjustment Factors): <strong>{round(100*st.session_state['adj_pd_av'], 3)}%</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Application Module Rating (Post Adjustment Factors): <strong>{st.session_state['adj_rating_av']}</strong></div>", unsafe_allow_html=True)

            gen_vars['Application Module Adjustment Factors']['PD'] = st.session_state['adj_pd_av']
            gen_vars['Application Module Adjustment Factors']['Rating'] = st.session_state['adj_rating_av']
            gen_vars['Customer Output']['PD'] = st.session_state['adj_pd_av']
            gen_vars['Customer Output']['Rating'] = st.session_state['adj_rating_av']

    return gen_vars

def ewi_calcs(weights_ewi, adj_df, av_bv_weights_fin, gen_vars):

    notch_cal, gen_vars = calculate_notches(weights_ewi, adj_df, 'Early Warning Indicators', gen_vars)
    gen_vars['Early Warning Indicators']['Notches'] = notch_cal
    
    cols = st.columns([0.2, 10, 0.2])
    with cols[1]: 
        if st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] == True:
    
            av_weight = av_bv_weights_fin['AV'][0]
            bv_weight = av_bv_weights_fin['BV'][0]

            # st.write(av_bv_weights_fin)
            st.session_state['comb_pd_pre_ewi'] = av_weight*st.session_state['adj_pd_av'] + bv_weight*st.session_state['overall_pd_bv']
            st.session_state['comb_rating_pre_ewi'] = get_rating_mrs(st.session_state['comb_pd_pre_ewi'])

            # st.write(st.session_state['comb_rating_pre_ewi'], st.session_state['comb_pd_pre_ewi'])

            mrs = st.session_state.mrs
            st.session_state['comb_pd_pre_ewi'] = mrs[mrs['Rating'] == st.session_state['comb_rating_pre_ewi']]['Mid'].iloc[0]
            
            mrs = st.session_state.mrs
            current_rating_index = mrs.index[mrs['Rating'] == st.session_state['comb_rating_pre_ewi']][0]
            new_rating_index = int(max(int(min(current_rating_index-notch_cal, len(mrs) - 1)), 0))
            
            if new_rating_index != current_rating_index:
                st.session_state['comb_pd_post_ewi'] = mrs[new_rating_index:new_rating_index+1]['Mid'].iloc[0]
                st.session_state['comb_rating_post_ewi'] = mrs[new_rating_index:new_rating_index+1]['Rating'].iloc[0]
            
            else:
                st.session_state['comb_pd_post_ewi'] = st.session_state['comb_pd_pre_ewi']
                st.session_state['comb_rating_post_ewi'] = st.session_state['comb_rating_pre_ewi']
    
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Notch Adjustment: <strong>{int(notch_cal)}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Customer PD (Post Early Warning Indicator and Pre Industry Module): <strong>{round(100*st.session_state['comb_pd_post_ewi'], 3)}%</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Customer Rating (Post Early Warning Indicator and Pre Industry Module): <strong>{st.session_state['comb_rating_post_ewi']}</strong></div>", unsafe_allow_html=True)

            gen_vars['Early Warning Indicators']['PD'] = st.session_state['comb_pd_post_ewi']
            gen_vars['Early Warning Indicators']['Rating'] = st.session_state['comb_rating_post_ewi']
            
            gen_vars['Customer Output']['PD'] = st.session_state['comb_rating_post_ewi']
            gen_vars['Customer Output']['Rating'] = st.session_state['comb_rating_post_ewi']
            

    return gen_vars


def calculate_notches(df, adj_df, var_type, gen_vars):

    gen_vars[var_type] = {}

    temp_range = adj_df[adj_df['Modification Variables'].isin(df['Variable Name'])].reset_index(drop = True)
    
    st.markdown("""
        <style>.small-font {
            font-size:25px !important;
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
        
    st.markdown(f'<p class="small-font">{var_type}</p>', unsafe_allow_html=True)
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)

    df['Notch'] = 0
    
    for i in range(0, len(df)):
        var = df['Variable Name'][i]
        var_weight = df['Weight'][i]
        af_choice = adj_df[adj_df['Modification Variables'] == var].reset_index(drop = True)

        cols = st.columns([0.2, 5, 5, 0.2])
        with cols[1]:
            st.write(f'{var}:')
            
        with cols[2]:
            st.markdown("""
            <style>
            .stSelectbox {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            </style>
            """, unsafe_allow_html=True)
            
            val = st.selectbox(label = '', options = list(af_choice['Attributions/Ranges']), index=0, key=f'{var}_afs')
            gen_vars[var_type][var] = val

            notch = adj_df[(adj_df['Modification Variables'] == var) & (adj_df['Attributions/Ranges'] == val)]['Notch'].iloc[0]

            df.loc[df['Variable Name'] == var, 'Notch'] = notch

    notch_cal = round(np.sum(df['Weight']*df['Notch']), 0)

    return notch_cal, gen_vars


def pd_rating_cals(weights, var_type, gen_vars, av_bv_weights_fin, prod_type, model_id, cust_id):

    # if f'button-{var_type}' not in st.session_state:
    st.session_state[f'button-{var_type}'] = False
# if f'overall_pd_{var_type}' not in st.session_state:
    st.session_state[f'overall_pd_{var_type}'] = None
# if f'overall_rating_{var_type}' not in st.session_state:
    st.session_state[f'overall_pd_{var_type}'] = None

    st.markdown("""
        <style>.small-font {
            font-size:25px !important;
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

    if var_type == 'av':
        cat_name = 'Application Variables'
        av_bv_col = 'AV'
    else:
        cat_name = 'Behavioral Variables'
        av_bv_col = 'BV'

    gen_vars[cat_name] = {}
    gen_vars[cat_name]['Weight'] = av_bv_weights_fin[av_bv_col][0]
    gen_vars[cat_name]['PD'] = None
    gen_vars[cat_name]['Rating'] = None
    # gen_vars['Behavioral Variables Weight'] = av_bv_weights_fin['BV'][0]
        
    st.markdown(f'<p class="small-font">{cat_name}</p>', unsafe_allow_html=True)
    
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)
    
    for i in range(0, len(weights)):
        var = weights['Variable Name'][i]
        var_weight = weights['Weight'][i]
        temp_range = st.session_state.var_ranges[st.session_state.var_ranges['Variable Name'] == var].reset_index(drop = True)
        d_type = pd.unique(temp_range['Var Type'])
        cols = st.columns([0.2, 5, 5, 0.2])
        
        if f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}' not in st.session_state:
            st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}'] = None

        if f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_{var}' not in st.session_state:
            st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_{var}'] = None
        
        if (d_type == 'Numeric'):
            if (temp_range['Lower'][0] == 0):
                temp_range['Lower'] = temp_range['Lower'].astype(float)
                min_value = 0
                
            else:
                temp_range['Lower'][0] = -1*np.inf
                temp_range['Lower'] = temp_range['Lower'].astype(float)
                min_value = None
        
        
        with cols[1]:
            st.write(f'{var}:')
            
        with cols[2]:
            if d_type == 'Numeric':
                step = max_step(temp_range)
                st.markdown("""
                <style>
                .stNumberInput {
                    margin-top: -45px;  /* Adjust the negative margin as needed */
                }
                </style>
                """, unsafe_allow_html=True)
                if min_value == 0:
                    min_value = float(f"{0:.{step}f}")
                
                val = st.number_input(label = '', min_value = min_value, step = 0.1 ** step, key = f'{var}_{cat_name}', format=f"%0.{step}f")
                st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}'] = temp_range[(val >= temp_range['Lower']) & (val < temp_range['Upper'])]['PD'].iloc[0]

                gen_vars[cat_name][var] = {}
                gen_vars[cat_name][var]['Value'] = val
                gen_vars[cat_name][var]["PD"] = st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}']
                gen_vars[cat_name][var]["Weight"] = var_weight
                gen_vars[cat_name][var]["Product"] = var_weight*st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}']
                # st.write(st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}'])
        
            else:
                st.markdown("""
                <style>
                .stSelectbox {
                    margin-top: -45px;  /* Adjust the negative margin as needed */
                }
                </style>
                """, unsafe_allow_html=True)
        
                val = st.selectbox(label = '', options = list(temp_range['Lower']), index=0, key=f'{var}')
                if val!= None:
                    st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}'] = temp_range[temp_range['Lower'] == val]['PD'].iloc[0]

                # gen_vars[cat_name][var] = val
                gen_vars[cat_name][var] = {}
                gen_vars[cat_name][var]['Value'] = val
                gen_vars[cat_name][var]["PD"] = st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}']
                gen_vars[cat_name][var]["Weight"] = var_weight
                gen_vars[cat_name][var]["Product"] = var_weight*st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}']
        
        with cols[2]:
            if st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}'] != None:
                st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_{var}'] = st.session_state[f'{prod_type}_{cust_id}_{model_id}_{var_type}_pd_{var}']*var_weight

    null_keys = [key for key in st.session_state if key.startswith(f'{var_type}_pd_') and st.session_state[key] is None]

    cols = st.columns([0.2, 10, 0.2])
    with cols[1]:
        if st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] == True:
            # mrs = st.session_state.mrs
            st.session_state[f'overall_pd_{var_type}'] = sum(st.session_state[key] for key in st.session_state if key.startswith(f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_'))
            st.session_state[f'overall_rating_{var_type}'] = get_rating_mrs(st.session_state[f'overall_pd_{var_type}'])

            gen_vars[cat_name]['PD'] = st.session_state[f'overall_pd_{var_type}']
            gen_vars[cat_name]['Rating'] = st.session_state[f'overall_rating_{var_type}']
            gen_vars['Customer Output']['PD'] = st.session_state[f'overall_pd_{var_type}']
            gen_vars['Customer Output']['Rating'] = st.session_state[f'overall_rating_{var_type}']
            
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>{cat_name} PD: <strong>{round(100*st.session_state[f'overall_pd_{var_type}'], 3)}%</strong></strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>{cat_name} Rating: <strong>{st.session_state[f'overall_rating_{var_type}']}</strong></div>", unsafe_allow_html=True)

    # st.write(st.session_state[key] for key in st.session_state if key.startswith(f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_'))
    # st.write(list(key for key in st.session_state if key.startswith(f'{prod_type}_{cust_id}_{model_id}_{var_type}_weight_pd_')))

    return gen_vars


def industry_overlay(gen_vars):

    gen_vars['Indutry Module'] = {}
    
    st.markdown("""
        <style>.small-font {
            font-size:25px !important;
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
        
    st.markdown(f'<p class="small-font">Industry Overlay</p>', unsafe_allow_html=True)
    st.markdown(f"<div class='boldhr'</div>", unsafe_allow_html=True)

    variables = ['Industry', 'Outlook Choice']

    modules = ['Module MENA Outlook', 'User UAE Outlook - Strong Upturn', 'User UAE Outlook - Upturn', 'User UAE Outlook - Stable', 'User UAE Outlook - Downturn', 'User UAE Outlook - Strong Downturn']

    for var in variables:
        cols = st.columns([0.2, 5, 5, 0.2])
        with cols[1]:
            st.write(f'{var}:')
            
        with cols[2]:
            st.markdown("""
            <style>
            .stSelectbox {
                margin-top: -45px;  /* Adjust the negative margin as needed */
            }
            </style>
            """, unsafe_allow_html=True)

            if var == 'Industry':
                ind = st.selectbox(label = '', options = list(st.session_state.industry_overlay['Industry Outlook']), index=0, key=f'{var}_im')
                gen_vars['Indutry Module'][var] = ind
            else:
                val = st.selectbox(label = '', options = modules, index=3, key=f'{var}_im')
                gen_vars['Indutry Module'][var] = val

    notch_cal = st.session_state.industry_overlay[(st.session_state.industry_overlay['Industry Outlook'] == ind)][val].iloc[0]
    gen_vars['Indutry Module']['Notches'] = notch_cal

    cols = st.columns([0.2, 10, 0.2])
    with cols[1]:
        if st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] == True:
            
            mrs = st.session_state.mrs
            current_rating_index = mrs.index[mrs['Rating'] == st.session_state['comb_rating_post_ewi']][0]
            new_rating_index = int(max(int(min(current_rating_index-notch_cal, len(mrs) - 1)), 0))
            # st.write(new_rating_index,current_rating_index)
            
            if new_rating_index != current_rating_index:
                st.session_state['comb_pd_post_im'] = mrs[new_rating_index:new_rating_index+1]['Mid'].iloc[0]
                st.session_state['comb_rating_post_im'] = mrs[new_rating_index:new_rating_index+1]['Rating'].iloc[0]
            
            else:
                st.session_state['comb_pd_post_im'] = st.session_state['comb_pd_post_ewi']
                st.session_state['comb_rating_post_im'] = st.session_state['comb_rating_post_ewi']
    
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Notch Adjustment: <strong>{int(notch_cal)}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Customer PD (Post Early Warning Indicator, Post Industry Module): <strong>{round(100*st.session_state['comb_pd_post_im'], 3)}%</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16px; padding-left: 10px; background-color: #b3c3d9; color: Black; padding-top: 1px;'>Customer Rating (Post Early Warning Indicator and Post Industry Module): <strong>{st.session_state['comb_rating_post_im']}</strong></div>", unsafe_allow_html=True)

            gen_vars['Indutry Module']['PD'] = st.session_state['comb_pd_post_im']
            gen_vars['Indutry Module']['Rating'] = st.session_state['comb_rating_post_im']
            gen_vars['Customer Output']['PD'] = st.session_state['comb_pd_post_im']
            gen_vars['Customer Output']['Rating'] = st.session_state['comb_rating_post_im']

    return gen_vars



# def clear_cr_inputs():
#     st.session_state['cust_id'] = ''
#     st.session_state['prod_type'] = None





def cr_page():
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
            margin-bottom: 0px;
    </style>
    """,
    unsafe_allow_html=True,
    )

    cr_sidebar()
    
    st.markdown(f'<p class="big-font">Rate a Customer</p>', unsafe_allow_html=True)

    st.session_state.var_ranges = pd.read_excel('Ranges.xlsx')
    st.session_state.mrs = pd.read_excel('Ranges.xlsx', sheet_name = 'MRS')
    st.session_state.adjustment_factors = pd.read_excel('Ranges.xlsx', sheet_name = 'Adjustments')
    st.session_state.ewi = pd.read_excel('Ranges.xlsx', sheet_name = 'EWI')
    st.session_state.av_bv_weight = pd.read_excel('Weight Transition.xlsx')
    st.session_state.industry_overlay = pd.read_excel('Industry Overlay.xlsx')
    if 'cust_id_cr' not in st.session_state:
        st.session_state.cust_id_cr = ''
    if 'prod_type_cr' not in st.session_state:
        st.session_state.prod_type_cr = None
        
    cust_prod_exists = 0

    customer_rating = pd.read_excel('Customer Rating.xlsx')

    # Generic Details
    av_bv_weights_fin, gen_vars = gen_details()
    # st.write(gen_vars)

    # st.write(gen_vars)
    model_state = pd.read_excel('assign_forms.xlsx', sheet_name = 'model_state')
    # st.write(list(model_state['model_id']))
    if (st.session_state['prod_type_cr'] != None) and (st.session_state['prod_type_cr'] not in list(model_state['product'])):
        # st.write
        cols = st.columns([0.2, 10, 0.2])
        with cols[1]:
            st.markdown(f"""
                        <div style='text-align: left; 
                        background-color: #FFE7E7; 
                        color: #6E0202;
                        padding-left: 10px;'>
                        <ul><li>{f'Model not deployed for {st.session_state.prod_type_cr}. Check with Model Development team.'}</li></ul>
                        </div>
                        """, unsafe_allow_html=True)

    if st.session_state['prod_type_cr'] == None:
        cols = st.columns([0.2, 10, 0.2])
        with cols[1]:
            st.markdown(f"""
                        <div style='text-align: left; 
                        background-color: #FFE7E7; 
                        color: #6E0202;
                        padding-left: 10px;'>
                        <ul><li>{f'Select Product'}</li></ul>
                        </div>
                        """, unsafe_allow_html=True)

    
    if st.session_state['cust_id_cr'] == '':
        cols = st.columns([0.2, 10, 0.2])
        with cols[1]:
            st.markdown(f"""
                        <div style='text-align: left; 
                        background-color: #FFE7E7; 
                        color: #6E0202; 
                        padding-left: 10px;'>
                        <ul><li>{f'Enter Customer ID'}</li></ul>
                        </div>
                        """, unsafe_allow_html=True)
    
    if len(customer_rating[(customer_rating['customer_id'] == st.session_state.cust_id_cr) & (customer_rating['product'] == st.session_state.prod_type_cr)]) != 0:
        cols = st.columns([0.2, 10, 0.2])
        with cols[1]:
            st.markdown(f"""
                        <div style='text-align: left; 
                        background-color: #FFE7E7; 
                        color: #6E0202; 
                        padding-left: 10px;'>
                        <ul><li>Rating for {st.session_state.cust_id} exists for {st.session_state.prod_type}.</li></ul>
                        </div>
                        """, unsafe_allow_html=True)
        cust_prod_exists = 1
    
    if (st.session_state['prod_type_cr'] != None) and (st.session_state['cust_id_cr'] != '') and (st.session_state['prod_type_cr'] in list(model_state['product'])) and (cust_prod_exists == 0):

        if f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}' not in st.session_state:
            st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] = False
        
        
        weights = pd.read_excel('Weights.xlsx', sheet_name = 'Weights Agg')
        weights = weights[(weights['Active'] == 1) & (weights['Product'] == st.session_state['prod_type_cr'])].reset_index(drop = True)
        model_id = weights['Model ID'][0]

        # Application Variables
        if len(weights[~weights['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])].reset_index(drop = True)) != 0:
            gen_vars = pd_rating_cals(weights[~weights['Category'].isin(['Behavioral Variables', 'Adjustments / Downgrade Factors', 'Early Warning Indicators'])].reset_index(drop = True), 'av', gen_vars, av_bv_weights_fin, st.session_state.prod_type_cr, model_id, st.session_state.cust_id_cr)
    
        # Application Module Adjustments / Downgrade Factors
        if len(weights[weights['Category'] == 'Adjustments / Downgrade Factors'].reset_index(drop = True)) != 0:
            weights_af = weights[weights['Category'] == 'Adjustments / Downgrade Factors'].reset_index(drop = True)
            gen_vars = adj_factors(weights_af, st.session_state.adjustment_factors, gen_vars)

        # st.write(av_bv_weights_fin)
        # Behavioral Variables
        if len(weights[weights['Category'] == 'Behavioral Variables'].reset_index(drop = True)) != 0:
            gen_vars = pd_rating_cals(weights[weights['Category'] == 'Behavioral Variables'].reset_index(drop = True), 'bv', gen_vars, av_bv_weights_fin, st.session_state.prod_type_cr, model_id, st.session_state.cust_id_cr)
    
        # Early Warning Indicators
        if len(weights[weights['Category'] == 'Early Warning Indicators'].reset_index(drop = True)) != 0:
            weights_ewi = weights[weights['Category'] == 'Early Warning Indicators'].reset_index(drop = True)
            gen_vars = ewi_calcs(weights_ewi, st.session_state.ewi, av_bv_weights_fin, gen_vars)
        
        # Industry Module
        gen_vars = industry_overlay(gen_vars)

        st.write('')
        st.write(gen_vars)
        
        if st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] == False:

            cols_delete = st.columns(5)
            ChangeButtonColour('Compute', 'black', '#b3c3d9', '5px', False, '5px', '-40px', '0px')
            if cols_delete[2].button('Compute', key=f'compute_scorecard'):
                st.session_state[f'compute_rating_pd_{st.session_state.cust_id_cr}_{st.session_state.prod_type_cr}'] = True
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()

        else:
            cols_delete = st.columns(5)
            ChangeButtonColour('Save', 'black', '#b3c3d9', '5px', False, '20px', '-40px', '0px')
            if cols_delete[2].button('Save', key=f'save_scorecard'):

                temp_df_list = [datetime.now(), st.session_state.cust_id_cr, st.session_state.prod_type_cr, model_id, gen_vars, gen_vars['Customer Output']['Rating'], st.session_state.email]
                temp_df = pd.DataFrame(temp_df_list).T
                temp_df.columns = customer_rating.columns
                
                customer_rating = pd.concat([customer_rating, temp_df]).reset_index(drop = True)
                customer_rating.to_excel('Customer Rating.xlsx', index=False)

                del st.session_state.cust_id_cr
                del st.session_state.prod_type_cr

                cols = st.columns([0.2, 10, 0.2])
                with cols[1]:
                    show_prompt_for_seconds(3, 'The customer has been rated.', '0px')
                
                st.session_state.page = 'cr_page'
                st.session_state.need_rerun = True
                if st.session_state.need_rerun:
                    st.session_state.need_rerun = False
                    st.rerun()










