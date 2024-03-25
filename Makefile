install_requirements:
	@pip install -r requirements.txt


#======================#
#       Streamlit      #
#======================#

streamlit: streamlit_local

streamlit_local:
	-@API_URI=local_api_uri streamlit run app.py

streamlit_local_docker:
	-@API_URI=local_docker_uri streamlit run app.py

streamlit_cloud:
	-@API_URI=cloud_api_uri streamlit run app.py
