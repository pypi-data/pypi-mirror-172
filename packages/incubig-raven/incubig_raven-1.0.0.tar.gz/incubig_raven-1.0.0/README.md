#raven documentation
This module is used to send secured communication to incubig clients.

The function takes following inputs
- [Optional][credentials] - Credentials in a .env file @ root directory
- [Mandatory][email_content] - A json object containing email subject, body and corresponding HTML
- [Optional][attachment] - A JSON object ({"data":file,"name":name,"type":type})
- [Mandatory][email_recipients] - A JSON object ({"to":[{"email":"example@example.com"},"display_name":"Display Name"],"cc":[{"email":"example@example.com"},"display_name":"Display Name"]."bcc":[{"email":"example@example.com"},"display_name":"Display Name"]})
