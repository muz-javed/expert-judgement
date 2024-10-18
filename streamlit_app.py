import numpy as np
import pandas as pd
import streamlit as st
from functions_admin import initialize_states, login_screen, admin_home, admin_roles, admin_models, pending_page_users, cr_page, view_model_report, calibrate_model
from functions_model_development import delphi_questionnaire_p1, delphi_questionnaire_p2, delphi_verification_form, delphi_shortlist_var, ahp_questionnaire, show_ahp_weight, ahp_weights_agg

from functions_admin import ChangeButtonColour

def main():

    initialize_states()
    
    if st.session_state.page == 'login':
        login_screen()

    if st.session_state.page == 'cr_page':
        cr_page()

    if st.session_state.page == 'admin_home':
        admin_home()

    if st.session_state.page == 'admin_roles':
        admin_roles()

    if st.session_state.page == 'admin_models':
        admin_models()

    if st.session_state.page == 'view_model_report':
        view_model_report(st.session_state.model_id, st.session_state.prod_type)

    if st.session_state.page == 'admin_responses':
        admin_responses()  

    if st.session_state.page == 'pending_page_user':
        pending_page_users()

    if st.session_state.page == 'delphi_p1':
        delphi_questionnaire_p1(st.session_state['team'], st.session_state['product'], st.session_state['model_id'])

    if st.session_state.page == 'delphi_p2':
        delphi_questionnaire_p2(st.session_state['team'], st.session_state['product'], st.session_state['model_id'])
        
    if st.session_state.page == 'delphi_ver':
        delphi_verification_form()

    if st.session_state.page == 'delphi_short_list_vars':
        delphi_shortlist_var()

    if st.session_state.page == 'ahp_questionnaire':
        ahp_questionnaire(st.session_state['team'], st.session_state['model_id'], st.session_state['shortlisted_vars'])


    if st.session_state.page == 'ahp_questionnaire_description':

        st.markdown("""
        <style>
        .main .block-container {
            max-width: 75%;
        }
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            margin-bottom: 0px;
        }
        </style>
        """, unsafe_allow_html=True)

        # cols = st.columns([0.01, 12])
        # with cols[1]:
        st.markdown(f'<p class="big-font" style = "margin-top: -40px">Hierarchal Tree for Variables</p>', unsafe_allow_html=True)
        # st.markdown(f'<p class="big-font">Product: {st.session_state.product}</p>', unsafe_allow_html=True)
        st.image('AHP Process.png')

        cols_button = st.columns(4)
        ChangeButtonColour('Back', 'black', '#b3c3d9', '20px', margin_top = '50px')
        if cols_button[1].button('Back', key='desc_page_back'):
            st.session_state['page'] = 'pending_page_user'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()

        ChangeButtonColour('Start Questionnaire', 'black', '#b3c3d9', '20px', margin_top = '50px')
        if cols_button[2].button('Start Questionnaire', key='desc_page_next'):
            st.session_state['page'] = 'ahp_questionnaire'
            st.session_state.need_rerun = True
            st.session_state.need_rerun = False
            st.rerun()


    if st.session_state.page == 'ahp_questionnaire_weights':
        df = st.session_state[f'ahp_weights_{st.session_state['team']}'].sort_values(['Model ID', 'Team', 'Category', 'Level']).reset_index(drop = True)
        show_ahp_weight(st.session_state['team'], df)

    if st.session_state.page == 'ahp_weights_agg':
        ahp_weights_agg(st.session_state.model_id)


    if st.session_state.page == 'calibrate_model':
        calibrate_model()
        




if __name__ == "__main__":
    main()















































# import streamlit as st
# import time

# def img_title(img_file_path):
#     cols = st.columns([1, 2, 1])

#     with cols[0]:
#         st.image(img_file_path, width=80)  
        
#     with cols[1]:
#         st.markdown("""
#             <style>
#             .text {
#                 font-size: 40px;
#                 font-weight: bold;
#                 margin-top: 30px;  /* Adjust the value as needed for white space */
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 text-align: center;
#             }
#             </style>
#             <div class="text">SME Expert Judgement Model</div>
#             """, unsafe_allow_html=True)
#         st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

# st.markdown(
# """
# <style>
# .main .block-container {
#     max-width: 70%;
#     padding-left: 1%;
#     padding-right: 1%;
# }
# </style>
# """,
# unsafe_allow_html=True,
# )

# img_title("EY Logo.png")





# with st.sidebar:
#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("The form has been submitted \n Redirecting back to homepage"):
#         time.sleep(3)
#         st.success("Done!")

# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )



# st.write(1)
