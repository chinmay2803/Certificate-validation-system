import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

# Streamlit options for certificate verification
options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    
    if uploaded_file is not None:
        # Save the uploaded PDF file locally
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        
        try:
            # Extract certificate data from the PDF
            (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            
            # Remove the PDF file after processing
            os.remove("certificate.pdf")

            # Generate the certificate ID hash
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # Smart Contract Call to verify the certificate
            result = contract.functions.isVerified(certificate_id).call()
            
            # Check the smart contract result and show appropriate message
            if result:
                st.success("Certificate validated successfully!")
            else:
                st.error("Invalid Certificate! The certificate might be tampered with.")
        
        except Exception as e:
            # Catch any exception and show an error message
            st.error(f"Error: {str(e)}")
            st.error("Invalid Certificate! The certificate might be tampered with.")

elif selected == options[1]:
    # Fix for the label warning by giving a proper label and hiding it using label_visibility
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID", label_visibility="visible")
    
    # Validate button
    submit = form.form_submit_button("Validate")
    
    if submit:
        try:
            # Display the certificate details based on the ID
            view_certificate(certificate_id)
            
            # Smart Contract Call to check if the certificate ID is valid
            result = contract.functions.isVerified(certificate_id).call()
           

            # Check the smart contract result and show appropriate message
            if result:
                st.success("Certificate validated successfully!")
            else:
                st.error("Invalid Certificate ID!")
        
        except Exception as e:
            # Catch any exception and show an error message
            st.error(f"Error: {str(e)}")
            st.error("Invalid Certificate ID!")