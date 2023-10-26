from zeep import Client

# On créer un client Zeep pour le service SOAP
client = Client('http://localhost:8000/client_service/?wsdl')  

# L'ID du client à interroger
client_id = "JohnDoe" 

# On appelle le service d'extraction de données client
personal_data = client.service.get_personal_data(client_id)
financial_data = client.service.get_financial_data(client_id)
property_data = client.service.get_property_data(client_id)

# On appelle le service de décision
decision = client.service.make_decision(client_id, property_data)

# On affiche les résultats
print("Données personnelles:")
print(f"Nom: {personal_data.nom}")
print(f"Adresse: {personal_data.adresse}")
print(f"Email: {personal_data.email}")
print(f"Téléphone: {personal_data.telephone}")

print("\nDonnées financières:")
print(f"Montant du prêt: {financial_data.montant_pret}")
print(f"Durée du prêt: {financial_data.duree_pret}")
print(f"Revenu mensuel: {financial_data.revenu_mensuel}")
print(f"Dépenses mensuelles: {financial_data.depenses_mensuelles}")

print("\nDonnées de propriété:")
print(f"Description de la propriété: {property_data.description_propriete}")
print(f"Montant du prêt associé à la propriété: {property_data.montant_pret}")

print("\nDécision d'attribution de prêt:")
print(decision)


print("####################")

# On appelle le 2eme Client
client_id2 = "JaneSmith"  

personal_data2 = client.service.get_personal_data(client_id2)
financial_data2 = client.service.get_financial_data(client_id2)
property_data2 = client.service.get_property_data(client_id2)

decision2 = client.service.make_decision(client_id2, property_data2)
print(f"Nom: {personal_data2.nom}")
print("\nDécision d'attribution de prêt:")
print(decision2)


print("####################")
#On appelle le 3eme Client
client_id3 = "AliceJohnson" 

personal_data3 = client.service.get_personal_data(client_id3)
financial_data3 = client.service.get_financial_data(client_id3)
property_data3 = client.service.get_property_data(client_id3)

decision3 = client.service.make_decision(client_id3, property_data3)
print(f"Nom: {personal_data3.nom}")
print("\nDécision d'attribution de prêt:")
print(decision3)