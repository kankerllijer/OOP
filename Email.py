import smtplib

email = " " #Email en donde generaste tu contraseña 
receiver_email = input("Para Email: ")

asunto = input("Asunto: ")
mensaje = input("Mensaje: ")


email_message = f"Subject: {asunto}\nFrom: {email}\nTo: {receiver_email}\n\n{mensaje}"

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email, " ") #contraseña generada por google 
        server.sendmail(email, receiver_email, email_message)

        print("Email enviado a " + receiver_email)
except:
  print("Error: No se pudo enviar el correo")
