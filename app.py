from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import mysql.connector
import streamlit as st
import os


import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn= mysql.connector.connect(host="localhost", user="root", passwd="xxxxxx",database=db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows
          #     table has the following columns-
## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name music_store and has the following table - album, album2,artist,customer
    employee,genre,invoice,invoice_line,media_type,playlist,playlist_track,track. album table has the 
    following columns- album_id,title,artist_id. album2 has the following columns-album_id,title,artist_id.
    artist table has the following columns- artist_id,name. customer table has the following columns-
    customer_id,first_name,last_name,company,address,city,state,country,postal_code,phone,fax,email,
    support_rep_id.employee table has the following columns-  employee_id,last_name,first_name,title,
    reports_to,levels,birthdate,hire_date,address,city,state,country,postal_code,phone,fax,email. genre 
    table has the following columns- genre_id,name . invoice table has the following columns- invoice_id,
    customer_id,invoice_date,billing_address,billing_city,billing_state,billing_country,billing_postal_code,
    total. invoice_line table has the following columns- invoice_line_id,invoice_id,track_id,unit_price,
    quantity.Media_type table has the following columns- media_type_id,name. playlist table has the 
    following columns- playlist_id,name. playlist_track table has the following columns-playlist_id,
    track_id.track table has the following columns-track_id,name,album_id,media_type_id,genre_id,composer,
    milliseconds,bytes,unit_price.
    
    SECTION \n\nFor example,\nExample 1 - Who is the senior most employee based on job title? , 
    the SQL command will be something like this SELECT title, last_name, first_name FROM employee ORDER BY 
    levels DESC LIMIT 1;
    
    \nExample 2 - Which countries have the most Invoices?, 
    the SQL command will be something like SELECT COUNT(*) AS c, billing_country FROM invoice GROUP BY 
    billing_countryORDER BY c DESC; 
    
    \nExample 3 - What are top 3 values of total invoice?,
    the SQL command will be something like SELECT total FROM invoice ORDER BY total DESC;
    
    \nExample 4 - Which city has the best customers? We would like to throw a promotional Music Festival 
    in the city we made the most money. Write a query that returns one city that has the highest sum of 
    invoice totals. Return both the city name & sum of all invoice totals.
    the SQL command will be something like SELECT billing_city,SUM(total) AS InvoiceTotal FROM invoice
    GROUP BY billing_city ORDER BY InvoiceTotal DESC LIMIT 1;
  
    \nExample 5 - Who is the best customer? The customer who has spent the most money will be declared 
    the best customer. Write a query that returns the person who has spent the most money.
    the SQL command will be something like SELECT customer.customer_id, first_name, last_name, SUM(total) AS total_spending
    FROM customer JOIN invoice ON customer.customer_id = invoice.customer_id GROUP BY customer.customer_id
    ORDER BY total_spending DESC LIMIT 1;

    \nExample 6 -  Write query to return the email, first name, last name, & Genre of all Rock Music 
    listeners. Return your list ordered alphabetically by email starting with A.
    the SQL command will be something like SELECT DISTINCT email,first_name, last_name
    FROM customer JOIN invoice ON customer.customer_id = invoice.customer_id JOIN invoice_line ON 
    invoice.invoice_id = invoice_line.invoice_id WHERE track_id IN( SELECT track_id FROM track JOIN genre
    ON track.genre_id = genre.genre_id WHERE genre.name LIKE 'Rock') ORDER BY email;

    \nExample 7 - Let's invite the artists who have written the most rock music in our dataset. Write a 
    query that returns the Artist name and total track count of the top 10 rock bands.
    the SQL command will be something like SELECT artist.artist_id, artist.name,COUNT(artist.artist_id) 
    AS number_of_songs FROM track JOIN album ON album.album_id = track.album_id JOIN artist ON artist.artist_id = album.artist_id
    JOIN genre ON genre.genre_id = track.genre_id WHERE genre.name LIKE 'Rock' GROUP BY artist.artist_id
    ORDER BY number_of_songs DESC LIMIT 10;

 
    \nExample 8 - Write a query that determines the customer that has spent the most on music for each country. 
    Write a query that returns the country along with the top customer and how much they spent. 
    For countries where the top amount spent is shared, provide all customers who spent this amount.
    the SQL command will be something like  
    WITH Customter_with_country AS (
		SELECT customer.customer_id,first_name,last_name,billing_country,SUM(total) AS total_spending,
	    ROW_NUMBER() OVER(PARTITION BY billing_country ORDER BY SUM(total) DESC) AS RowNo 
		FROM invoice
		JOIN customer ON customer.customer_id = invoice.customer_id
		GROUP BY 1,2,3,4
		ORDER BY 4 ASC,5 DESC)
    SELECT * FROM Customter_with_country WHERE RowNo <= 1


    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"music_store")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)