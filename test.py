import requests

batch_id="750H1000005JFr3IAG"
url = f"https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v58.0/jobs/ingest/{batch_id}/batches"

payload = "LastName,EXT_ID__c \nNavin Reddy12,32453253201\nAjayaaaaa01,23453245301"
headers = {
  'Authorization': 'Bearer 00D0p0000000NBa!AQkAQHxIzGvqjbUDIX2BxKcF_IiOi1y85p_G9wTVw9u9IV5nCzNxCgj7ikWr.csUQQaeeT8YmA8L_BRfEakajgbfhUjFfn8L',
  'Content-Type': 'text/csv',
  'Accept': 'application/json',
  'Cookie': 'BrowserId=HzeVIY20Ee6wvYuF3JMXGA; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1; BrowserId=Dr1VWQ4BEe-ofSEQvz_zMQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1; BrowserId=R9e6DA6ZEe-ofSEQvz_zMQ; CookieConsentPolicy=0:1; LSKey-c$CookieConsentPolicy=0:1'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.status_code)

print(response.text)
