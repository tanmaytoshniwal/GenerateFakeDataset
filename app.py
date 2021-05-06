# Importing Packages
import streamlit as st 
import streamlit.components.v1 as stc
import pandas as pd 
import faker
from faker import Faker
import json
import base64
import time 
timestr = time.strftime("%Y%m%d-%H%M%S")


# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File ** ")
    new_filename = "fake_dataset_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)

# Fxn to Download Into A Format
def make_downloadable_df_format(data,format_type="csv"):
	if format_type == "csv":
		datafile = data.to_csv(index=False)
	elif format_type == "json":
		datafile = data.to_json(orient="table")
	b64 = base64.b64encode(datafile.encode()).decode()  # B64 encoding
	st.markdown("### ** Download File  📩 ** ")
	new_filename = "fake_dataset_{}.{}".format(timestr,format_type)
	href = f'<a href="data:file/{format_type};base64,{b64}" download="{new_filename}">Click Here!</a>'
	st.markdown(href, unsafe_allow_html=True)


# Generate A Simple Profile
def generate_profile(number,random_seed=200):
	fake = Faker()
	Faker.seed(random_seed)
	data = [fake.simple_profile() for i in range(number)]
	df = pd.DataFrame(data)
	return df


custom_title = '''<h1 style='color:white'>Fake Data Generator'''


def main():
	
	stc.html(custom_title)

	menu = ["Profile","Customize","About"]

	choice = st.sidebar.selectbox("Menu",menu)




	if choice == "Profile":
		st.subheader("Simple profile dataset!")

		number_to_gen = st.sidebar.number_input("Number",10,10000)
		dataformat = st.sidebar.selectbox("Save Data As",["csv","json"])

		# Initialize Faker Class
		custom_fake = Faker()
		data = [custom_fake.simple_profile() for i in range(number_to_gen)]
		df = pd.DataFrame(data)

		# View As Dataframe
		st.dataframe(df)

		# View as JSON
		with st.beta_expander("🔍: View JSON "):
			st.json(data)

		with st.beta_expander("📩: Download"):
			make_downloadable_df_format(df,dataformat)




	elif choice == "Customize":
		st.subheader("Customize your dataset!")
	
		options_list=['address', 'am_pm', 'boolean', 'city', 'city_prefix', 'city_suffix', 'color', 'color_name', 'company', 'company_email', 'country', 'country_calling_code', 'country_code',  'credit_card_number', 'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_name', 'csv', 'currency', 'currency_name', 'currency_symbol', 'date','day_of_month', 'day_of_week', 'email', 'file_extension', 'file_name', 'first_name', 'first_name_female', 'first_name_male', 'hex_color', 'http_method', 'json', 'last_name', 'last_name_female', 'last_name_male','license_plate','month_name','name', 'name_female', 'name_male','password',  'phone_number', 'postalcode','profile','random_digit', 'random_int', 'random_letter','rgb_color','user_name', 'url', 'zipcode']
		fields = st.sidebar.multiselect("Fields",options_list,default='name')

		number_to_gen = st.sidebar.number_input("Number",10,10000)
		dataformat = st.sidebar.selectbox("Save Data As",["csv","json"])
		
		df=pd.DataFrame()

		# Initialize Faker Class
		custom_fake = Faker()
		for stri in fields:
			data = [getattr(custom_fake,stri)() for i in range(number_to_gen)]
			dftemp = pd.DataFrame(data)
			dftemp.rename(columns = {0 : stri}, inplace = True)
			df=pd.concat([df,dftemp],axis=1)
			

		# View As Dataframe
		st.dataframe(df)
		res=df.to_json(orient="table")

		# View as JSON
		with st.beta_expander("🔍: View JSON "):
			st.json(res)


		with st.beta_expander("📩: Download"):
			make_downloadable_df_format(df,dataformat)
		



	else:
		st.subheader("About")
		st.success("Built with Streamlit")
		#st.info("Tanmay Toshniwal")
		st.text("By Tanmay Toshniwal")



if __name__ == '__main__':
	main()


