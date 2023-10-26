from spyne import Application, srpc, ServiceBase, Unicode, ComplexModel, Integer, Decimal, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

# Dictionnaire de clients
clients_data = {
    "JohnDoe": {
        "nom": "John Doe",
        "adresse": "123 Rue de la Liberté, 75001 Paris, France",
        "email": "john.doe@email.com",
        "telephone": "+33 123 456 789",
        "montant_pret": 200000,
        "duree_pret": 20,
        "revenu_mensuel": 5000,
        "depenses_mensuelles": 3000,
        "description_propriete": "Maison à deux étages avec jardin, située dans un quartier résidentiel calme."
    },
    "JaneSmith": {
        "nom": "Jane Smith",
        "adresse": "456 Oak Street, Los Angeles, USA",
        "email": "jane.smith@email.com",
        "telephone": "+1 555 123 456",
        "montant_pret": 100000,
        "duree_pret": 5,
        "revenu_mensuel": 6000,
        "depenses_mensuelles": 5000,
        "description_propriete": "Appartement en centre-ville."
    },
    "AliceJohnson": {
        "nom": "Alice Johnson",
        "adresse": "789 Elm Avenue, London, UK",
        "email": "alice.johnson@email.com",
        "telephone": "+44 20 1234 5678",
        "montant_pret": 100000,
        "duree_pret": 25,
        "revenu_mensuel": 5500,
        "depenses_mensuelles": 4000,
        "description_propriete": "Maison de campagne avec grand jardin."
    }
}


class ClientData(ComplexModel):
    nom = Unicode
    adresse = Unicode
    email = Unicode
    telephone = Unicode

class FinancialData(ComplexModel):
    montant_pret = Integer
    duree_pret = Integer
    revenu_mensuel = Integer
    depenses_mensuelles = Integer

class PropertyData(ComplexModel):
    description_propriete = Unicode
    montant_pret = Integer

#Service d'extraction de données Client

class ServiceExtraction(ServiceBase):
    @srpc(Unicode, _returns=ClientData)
    def get_personal_data(client_id):
        client = clients_data.get(client_id, {})
        return ClientData(**client)

    @srpc(Unicode, _returns=FinancialData)
    def get_financial_data(client_id):
        client = clients_data.get(client_id, {})
        financial_data = {
            "montant_pret": client.get("montant_pret", 0),
            "duree_pret": client.get("duree_pret", 0),
            "revenu_mensuel": client.get("revenu_mensuel", 0),
            "depenses_mensuelles": client.get("depenses_mensuelles", 0)
        }
        return FinancialData(**financial_data)

    @srpc(Unicode, _returns=PropertyData)
    def get_property_data(client_id):
        client = clients_data.get(client_id, {})
        property_data = {
            "description_propriete": client.get("description_propriete", ""),
            "montant_pret": client.get("montant_pret", 0)
        }
        return PropertyData(**property_data)
    
#Service de vérification de solvabilité
class SolvencyService(ServiceBase):
    @srpc(FinancialData, _returns=Unicode)
    def check_solvency(financial_data):
        x = (financial_data.revenu_mensuel - financial_data.depenses_mensuelles) * 12
        y = financial_data.montant_pret / financial_data.duree_pret

        if x >= y:
            return "Le client est solvable."
        else:
            return "Le client n'est pas solvable."    
        


class ServiceEvaluationPropriete(ServiceBase):
    @srpc(PropertyData, _returns=Unicode)
    def evaluate_property(property_data):
        description_propriete = property_data.description_propriete
        montant_pret = property_data.montant_pret

        valeur_estimee = 100000
        if "jardin" in description_propriete:
            valeur_estimee += 10000
        if "piscine" in description_propriete:
            valeur_estimee += 50000
        if "centre-ville" in description_propriete:
            valeur_estimee += 5000

        # Comparez la valeur estimée à la valeur du prêt pour déterminer si la propriété vaut le montant du prêt.
        is_property_worth_loan = valeur_estimee >= montant_pret

        if is_property_worth_loan:
            return "La propriété vaut le montant du prêt."
        else:
            return "La propriété ne vaut pas le montant du prêt."


class ServiceDecision(ServiceBase):
    @srpc(Unicode, PropertyData, _returns=Unicode)
    def make_decision(client_id, property_data):
        solvability_result = SolvencyService.check_solvency(ServiceExtraction.get_financial_data(client_id))
        evaluation_result = ServiceEvaluationPropriete.evaluate_property(property_data)

        if solvability_result == "Le client est solvable." and evaluation_result == "La propriété vaut le montant du prêt.":
            return "L'acceptation de l'attribution du prêt."
        else:
            decision = "Refus de l'attribution du prêt."
            if solvability_result != "Le client est solvable.":
                decision += " Le client n'est pas solvable."
            if evaluation_result != "La propriété vaut le montant du prêt.":
                decision += " La propriété ne vaut pas le montant du prêt."
            return decision

if __name__ == '__main__':
    application = Application([ServiceExtraction, SolvencyService, ServiceEvaluationPropriete, ServiceDecision], 'client_service',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11()
                             )

    wsgi_application = WsgiApplication(application)

    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()