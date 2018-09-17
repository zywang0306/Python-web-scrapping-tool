import requests 
import re
from bs4 import BeautifulSoup as bs

#find the nth string that match the pattern
#the helper function for locating the data in the webpage
def search_for_nth(array,start_ind,n,pattern):
	count = 0
	current_ind = start_ind
    
        while(count < n):
        	current_ind += 1
                if array[current_ind] == pattern:
			count += 1

	return current_ind

#website url
prefix = 'http://amp.pharm.mssm.edu/Harmonizome/'

#make url string and link to the web
gene_url = prefix + 'gene_set/K562/Roadmap+Epigenomics+Cell+and+Tissue+Gene+Expression+Profiles'
gene_link = requests.get(gene_url)

#pattern of gene link
ref_pattern = re.compile('href="gene\/.*?"')

#pattern of range data
range_pattern = re.compile('\([0-9]*\.\.[0-9]*[\,|\)]')
counter = 0

gene_dict = {}

#open the file for writing
output_file = open("K562_expression", 'w')
output_file.write("Gene  Standard_Deviation \n")

#split the content and process
html_info = gene_link.content.split()
for i in range(0,len(html_info)):
    	info = html_info[i]
        
        #search for pattern
	if ref_pattern.search(info) is not None:
		counter += 1

		#print out the progress every 200 data points
		if counter % 200 == 0:
			print "finish " + str(counter) + " amount of data" 


		link_ID = info[6:-2]
		gene_name = html_info[i+1]
                
                #search and find the location of the data in the html_info based on a "reference string"
                reference_string = 'class="col-md-5">'
		second_point = search_for_nth(html_info,i,2,reference_string)
		std = float(html_info[second_point + 1])

		#write out each data
		output_file.write(gene_name + " " + str(std) + " \n")

output_file.close()


