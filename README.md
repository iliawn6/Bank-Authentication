# Bank Authentication System

This project implements a bank authentication system designed to verify user identities using facial recognition technology and cloud-based services. The system utilizes various services including a cloud-hosted backend, a MySQL database, object storage (S3), an image processing tool (IMGAA service), a message queuing service (RabbitMQ) and an email sender service. 


## System Workflow

1. **User Submission**: Users submit their individual information, such as email and national number, along with two images of their face.
2. **Data Storage**: The submitted information is stored in the MySQL database, and the images are uploaded to S3 storage.
3. **Queue Management**: The username is placed in a RabbitMQ queue to be processed by the second service.
4. **Image Processing**: The second service retrieves the images from S3 and uses the IMGAA service to check if both images are of a human face and to compare the similarity between the two images.
5. **Notification**: Once the images are verified and compared, the result (success or failure of authentication) is sent to the user via an email notification.


## Components

- **Backend Server**: Handles API requests for user data submission and serves as the communication layer between the front-end and other services.
- **MySQL Database**: Stores user data including emails and national numbers securely.
- **S3 Storage**: Used for storing user-submitted images.
- **RabbitMQ**: Manages message queueing between services to ensure reliable processing.
- **IMGAA Service**: Processes images to confirm they are of human faces and checks for similarities between the two submitted images.
- **Email Sender Service (Mailgun)**: Sends emails to users to notify them of the status of their authentication request.
