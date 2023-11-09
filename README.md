# Food Rescue Subscription Service

## Introduction

This repository hosts the Food Rescue Subscription Service, a Flask application designed to alert users about new food rescue opportunities. Whenever there is food that needs to be rescued immediately, this application listens to RabbitMQ messages and triggers an email notification to users who have opted in for alerts.

## Features

- **Real-Time Alerts**: Users receive email notifications for immediate food rescue opportunities.
- **RabbitMQ Integration**: Utilizes RabbitMQ for message listening to ensure timely notifications.
- **User Preference Activation**: Allows users to activate notification preferences to receive alerts.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- Flask
- Access to a RabbitMQ instance

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/GreenHarbor/foodrescuesubscription.git
   ```
2. Navigate to the project directory:
   ```
   cd foodrescuesubscription
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure your environment variables for RabbitMQ and the email service.

### Running the Application

1. To start the Flask application, run:
   ```
   flask run
   ```
2. The application will now be listening for messages from RabbitMQ and sending out email notifications as configured.

## Usage

- **Activate Notifications**: Users can activate their email notification preferences through the provided API endpoint.
- **Receive Alerts**: Once activated, users will receive email alerts for new food rescue opportunities.
