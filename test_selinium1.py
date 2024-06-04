from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Lists to store scraped data
doctor_names = []
doctor_links = []
specializations = []
licenses = []
edu_exper = []
user_exper = []
fees = []
about = []
u_loca = []

# Base URL of the website
base_url = "https://healthwire.pk"

# Function to scrape doctor details from the current page content
def scrape_doctor_details(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the div containing the doctor listings
    doctor_listings = soup.find_all("div", class_="doctor_listing_page_wraper_outer")
    doctor_listing1 = soup.select('.doctor-treat-outer_treating .doctor-treat')

    # Extracting data from doctor listings
    for listing in doctor_listings:
        # Find all h3 elements within the listing
        name_tags = listing.find_all("h3")
        for name_tag in name_tags:
            # Find the a tag within each h3 tag
            a_tag = name_tag.find("a")
            if a_tag:
                # Append the text of the a tag to the doctor_names list
                doctor_names.append(a_tag.text.strip())
                # Append the href link to the doctor_links list
                full_url = base_url + a_tag['href']
                doctor_links.append(full_url)
    
        # About 
        for u in doctor_links:
            page = requests.get(u)
            soup = BeautifulSoup(page.text, 'html.parser')
            about_title = soup.find("div", class_ = "comment more")
            if about_title:
                abt_tag = about_title.find("p")
                about.append(abt_tag.text.strip())
            else:
                about.append("About Title not found")

            location1 = soup.find("div", class_="locate-detail")
            if location1:
                lo_tag = location1.find("a")
                lo_tag = lo_tag.text.strip()
            else:
                lo_tag = "N/A"
                
            u_loca.append(lo_tag) 

        # Find all p elements within the listing for specialization
        feature_tags = listing.find_all("p")
        for f_t in feature_tags:
            specializations.append(f_t.text.strip())
        
        # Find all ul elements within the listing for licenses
        ul_tags = listing.find_all("ul")
        for ul_tag in ul_tags:
            li_tag = ul_tag.find("li", class_="pmc-verified")
            if li_tag:
                licenses.append(li_tag.text.strip())

        # Find all doctor educational and user experiences
        edu_experiences = listing.find_all("div", class_="education-experience")
        user_experiences = listing.find_all("ul", class_="doctor-user-experiance")
        for edu in edu_experiences:
            e_tag = edu.find("span", class_="education")
            if e_tag:
                edu_exper.append(e_tag.text.strip())
        for u_e in user_experiences:
            u_tag = u_e.find("li")
            if u_tag:
                user_exper.append(u_tag.text.strip().replace('\n', ' '))

        doctor_listings = soup.select('.doctor-treat-outer_treating .doctor-treat')

        for listing in doctor_listing1:
            # Extract fees
            fee_span = listing.select_one('.hospitals-slider .top-section .fees')
            if fee_span:
                fee = fee_span.text.strip()
            else:
                fee = "N/A"
            fees.append(fee)

# Specify the path to the new ChromeDriver if needed
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Replace with the URL of the website you are scraping
url = "https://healthwire.pk/doctors/lahore"

# Open the webpage
driver.get(url)

try:
    # Initialize counter variable
    counter = 0
    
    while counter < 5:
        try:
            # Wait for the "Load More Doctors" link to be present
            load_more_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "load-more-doctors"))
            )

            # Scroll the "Load More Doctors" link into view using JavaScript
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_link)

            # Optional: Wait for a brief moment to ensure the element is in view
            time.sleep(1)

            # Click the "Load More Doctors" link using JavaScript
            driver.execute_script("arguments[0].click();", load_more_link)

            # Optional: Wait for some time to allow new content to load
            time.sleep(3)
            
            # Scrape the doctor details from the current page
            scrape_doctor_details(driver.page_source)
            
            # Increment counter
            counter += 1
        except:
            # If the "Load More Doctors" link is not found, break the loop
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()

# Print or process scraped data as needed
print("Doctor Names:", doctor_names)
print("Specializations:", specializations)
print("Licenses:", licenses)
print("Educational Experience:", edu_exper)
print("User Experience:", user_exper)
print("Fees:", fees)
print("About:", about)
print("Locations:", u_loca)