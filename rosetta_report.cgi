#!/usr/local/bin/python
#
# Program: rosetta_report.cgi
#
# Purpose: This cgi supports TR4832, creating an online version of
#   W.K. Silvers "Coat Colors of Mice" book.
#
#   To create a table with the following columns:
#
#   1) Nomenclature of alleles used in W.K. Silvers' book
#
#   2) Their current nomenclature used in MGI
#
#   3) All phenotypic alleles for that gene 
#
#
# Requirements Satisfied by This Program: TR4832


import sys
import string
import cgi

# add the MGI standard library directory to the PythonPath so that we can find
# the standard Configuration.py and ignoreDeprecation modules:
MGI_LIBS = '/usr/local/mgi/live/lib/python'
if MGI_LIBS not in sys.path:
	sys.path.insert (0, MGI_LIBS)

# for now, ignore any deprecation errors that could be caused by the
# migration to Python 2.4.2 -- we'll fix them later
import ignoreDeprecation

import Configuration
config = Configuration.get_Configuration ('Configuration', 1)

import CGI
import mgi_html

class rosettaReportClass (CGI.CGI):
###########################################################
# Concept: Container class for methods used to create 
#   a rosettaStone table
# IS:   
# HAS: No parameters
# DOES: Creates the rosetta stone table used in
#   W.K. Silvers book
# Implementation: 

    # Row counter used for gray/white table shading 
    totalRowCount = 0

    def openRosettaPage(self):
    #######################################################
    # Purpose: To create a list strings which contain valid HTML
    #   used to return a page to the user
    # Returns: page (list of strings)
    # Assumes: Nothing
    # Effects: Nothing
    # Throws:  Nothing
    
        # Open page and add HTML page headings
        rosettaPage = [ '<HTML><HEAD>', '<TITLE>%s - ' % config['WKSTITLE'],
            '</TITLE>',
	    '</HEAD><BODY BGCOLOR="#FFFFFF">',
	    '<SCRIPT TYPE="text/javascript" SRC="%sjs/jquery-1.10.2.min.js"></SCRIPT>' % config['WEBSHARE_URL'],
            ]

        # Add banner
        rosettaPage.append (
        '<TABLE WIDTH="100%" BORDER=0 CELLPADDING=2 CELLSPACING=1 >'
            '<TR>'
                '<TD WIDTH="100%" BGCOLOR="#D0E0F0" ALIGN="center" VALIGN="center">'
                '<FONT COLOR="#000000" SIZE=5 FACE="Arial,Helvetica">'
                '<B>Coat Color Genes of the Mouse</B></FONT>'
                '</TD>'
            '</TR>'
        '</TABLE>')

        # Add descriptive text
        rosettaPage.append (
            '<H3>Adapted from '
            '<B><I>The Coat Colors of Mice</I></B> by Willys K. Silvers</H3>'
            '<P>The table lists those genes described in The Coat Colors of '
            'Mice (as of 1979), with their current nomenclature and links '
            'to a complete list of alleles for each of these genes. </P>'
            '<P>Please see also a <A HREF="'+ config['COATANOM'] + '" TARGET="_BLANK">table</A> '
            'of all currently known genotypes in MGI annotated with the phenotype '
            'term "coat color anomalies."</P>'
            )
        
        return rosettaPage
        

    def makeRosettaTable(self,rosettaPage):
    #######################################################
    # Purpose: Add the rosetta data table to the return page.
    # Returns: rosettaPage (list of strings)
    # Assumes: rosettaPage has already been opened and prepared with
    #   the required HTML tags
    # Effects: rosettaPage
    # Throws:  Nothing

    	rosettaPage.append('<DIV ID="rosettaDiv">Loading...</DIV>')

	rosettaPage.append('''<SCRIPT>
		$(document).ready(function(){
			$.ajax({ url: "%smarker/wksilversTable",
				success: function(data){
					$('#rosettaDiv').html(data);
				}});
			});
		</SCRIPT>''' % config['FEWI_URL'])

        return rosettaPage

    def main (self):
    #######################################################
    # Purpose: Driving routing of class.
    # Returns: Nothing
    # Assumes: Nothing
    # Effects: rosettaPage with is then returned to the user
    # Throws:  Nothing
    
        rosettaPage = self.openRosettaPage()
        
        rosettaPage = self.makeRosettaTable(rosettaPage)
        
        # Close the page
        rosettaPage.append ('<HR>')
        rosettaPage.append ('</BODY></HTML>')

        # output page to STDOUT
        for outputString in rosettaPage:
            print outputString
        
        return

################## 
### Main logic ###
##################
rosettaCGI = rosettaReportClass()

# the go() method from parent class simply wraps the main() in 
# error handling
rosettaCGI.go()
