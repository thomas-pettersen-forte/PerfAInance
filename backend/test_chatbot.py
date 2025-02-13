import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Last inn miljøvariabler
load_dotenv()

# Azure OpenAI-legitimasjon
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_API_VERSION")  
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")  

# Initialiser OpenAI-klient for Azure
client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
)

def get_financial_advice(income, debt, rent, insurance, subscriptions):
    """
    Sender brukerens økonomiske data til Azure OpenAI GPT-4o og returnerer økonomiske råd.
    """

    # Beregn disponibel inntekt
    totale_utgifter = debt + rent + insurance + subscriptions
    disponibel_inntekt = income - totale_utgifter

    # Chat prompt for GPT-4o
    prompt = f"""
    Brukeren har en årlig inntekt på {income} NOK før skatt.
    Deres årlige utgifter er:
    - Gjeld/Lån: {debt} NOK
    - Husleie: {rent} NOK
    - Forsikring: {insurance} NOK
    - Abonnementer: {subscriptions} NOK

    Deres **disponible inntekt** etter utgifter er **{disponibel_inntekt} NOK**.

    Basert på disse dataene, gi dem **3 personlige økonomiske forbedringstips** i **enkelt og vennlig språk**.
    Spør deretter om de trenger hjelp med spesifikke økonomiske emner som budsjettering, sparemål eller nedbetaling av lån.
    """

    try:
        response = client.chat.completions.create(
            model=deployment_name, 
            messages=[
                {"role": "system", "content": "Du er en hjelpsom økonomisk assistent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Skriv ut rå JSON-respons for debugging (valgfritt)
        print(response.model_dump_json(indent=2))

        return response.choices[0].message.content

    except Exception as e:
        return f"Feil: {str(e)}"

def continue_chat(previous_messages):
    """
    Fortsetter chatten basert på brukerens input.
    """
    while True:
        user_message = input("Du: ").strip()
        if user_message.lower() in ['exit', 'quit', 'avslutt']:
            print("👋 Takk for at du brukte den personlige økonomiske assistenten! Ha en fin dag!")
            break

        previous_messages.append({"role": "user", "content": user_message})

        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=previous_messages,
                temperature=0.7
            )

            # Skriv ut rå JSON-respons for debugging (valgfritt)
            print(response.model_dump_json(indent=2))

            assistant_message = response.choices[0].message.content
            print(f"Assistent: {assistant_message}")

            previous_messages.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            print(f"Feil: {str(e)}")

# Kjør chatbot i terminalen
if __name__ == "__main__":
    print("💰 Velkommen til din personlige økonomiske assistent! 💰")
    while True:
        try:
            income = float(input("Skriv inn din årlige inntekt før skatt (NOK): "))
            debt = float(input("Skriv inn dine årlige gjelds-/lånebetalinger (NOK): "))
            rent = float(input("Skriv inn din årlige husleie (NOK): "))
            insurance = float(input("Skriv inn dine årlige forsikringskostnader (NOK): "))
            subscriptions = float(input("Skriv inn dine årlige abonnementskostnader (NOK): "))

            print("\n🔎 Analyserer dine økonomiske data...\n")
            advice = get_financial_advice(income, debt, rent, insurance, subscriptions)

            print("🧠 Økonomiske råd:")
            print(advice)

            previous_messages = [
                {"role": "system", "content": "Du er en hjelpsom økonomisk assistent."},
                {"role": "user", "content": f"Brukeren har en årlig inntekt på {income} NOK før skatt. Deres årlige utgifter er: Gjeld/Lån: {debt} NOK, Husleie: {rent} NOK, Forsikring: {insurance} NOK, Abonnementer: {subscriptions} NOK. Deres disponible inntekt etter utgifter er {income - (debt + rent + insurance + subscriptions)} NOK."},
                {"role": "user", "content": advice}
            ]

            continue_chat(previous_messages)

            break

        except ValueError:
            print("❌ Vennligst skriv inn gyldige numeriske verdier for alle innspill.")

