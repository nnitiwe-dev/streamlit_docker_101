# Use an official Python image as the base
FROM python:3.8-slim-buster

# Set environment variables
ENV APP_HOME /app
ENV STREAMLIT_PORT 8501

# Set the working directory
WORKDIR $APP_HOME

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app source code into the container
COPY app $APP_HOME

# Expose the Streamlit app port
EXPOSE $STREAMLIT_PORT

# Specify the command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "$STREAMLIT_PORT"]
