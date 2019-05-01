
# Note Delete this latter 
# cust page widget will have a template attribute 
# this will be the identifier for the type of template to use
# then it will have list of values like the title, body, 




# Long meaningless piece of text
loremipsum_1 = """Lorem ipsum dolor sit amet, vel ne quando dissentias. Ne his opo\
rteat expetendis. Ei tantas explicari quo, sea vidit minimum menandri ea. His ca\
se errem dicam ex, mel eruditi tibique delicatissimi ut. At mea wisi dolorum con\
tentiones, in malis vitae viderer mel.
Vis at dolores ocurreret splendide. Noster dolorum repudiare vis ei, te augue su\
mmo vis. An vim quas torquatos, electram posidonium eam ea, eros blandit ea vel.\
Reque summo assueverit an sit. Sed nibh conceptam cu, pro in graeci ancillae co\
nstituto, eam eu oratio soleat instructior. No deleniti quaerendum vim, assum sa\
epe munere ea vis, te tale tempor sit. An sed debet ocurreret adversarium, ne en\
im docendi mandamus sea.
"""
loremipsum_2 = """Vis at dolores ocurreret splendide. Noster dolorum repudiare v\
is ei, te augue summo vis. An vim quas torquatos, electram posidonium eam ea, er\
os blandit ea vel. Reque summo assueverit an sit. Sed nibh conceptam cu, pro in \
graeci ancillae constituto, eam eu oratio soleat instructior. No deleniti quaere\
ndum vim, assum saepe munere ea vis, te tale tempor sit. An sed debet ocurreret \
adversarium, ne enim docendi mandamus sea.
"""

class Templates:
    '''The Template class contain defferent pdf
    format template'''

    def __init__(self, pdf_cls):
        self.pdf = pdf_cls


    def template1(self, title='', body=''):
        pdf = self.pdf
        pdf.add_page()

        effective_page_width = pdf.w - 2*pdf.l_margin

        if title is not None:     #if title specified set title
            pdf.set_font('Times','b',20)
            pdf.cell(effective_page_width,0.0, title, align='C')
            pdf.ln(15)

        # create the body
        pdf.set_font('Times','',10.0)
        pdf.multi_cell(effective_page_width, 10, body)


    def template2(self, title='', body_1='', body_2=''):   
        pdf = self.pdf
        pdf.add_page()

        #padding for the double multiline text
        padding = 2


        effective_page_width = pdf.w - 2*pdf.l_margin

        if title is not None:     #if title specified set title
            pdf.set_font('Times','b',20)
            pdf.set_font('Times','b',20)
            pdf.cell(effective_page_width,0.0, title, 'U', align='C')
            pdf.ln(15)

        
        #set font for body
        pdf.set_font('Times','',10.0)
        
        # First save the y coordinate just before rendering the first multi_cell
        ybefore = pdf.get_y()
        pdf.set_x(pdf.l_margin - padding)

        pdf.multi_cell(effective_page_width/2, 8, body_1)


        # Notice the use of "effective_page_width/2 + pdf.l_margin" as x to position
        # the cursor horizontally just beyond the first multi_cell

        pdf.set_xy(effective_page_width/2 + pdf.l_margin + padding, ybefore)
        pdf.multi_cell(effective_page_width/2, 8, body_2)
        

    def template3(self, title='', author=''):
        pdf = self.pdf
        pdf.add_page()

        effective_page_width = pdf.w - 2*pdf.l_margin

        pdf.set_font('Times', 'b', 22)

        pdf.set_y(100)
        pdf.cell(effective_page_width, 0, title, align='C')

        pdf.ln(15)

        pdf.set_font('Times', 'i', 15)
        pdf.cell(effective_page_width, 0, author, align='C')


from fpdf import FPDF

class UniCloudPdf(FPDF):

    def header(self):
        #self.image('/root/.kivy/icon/kivy-icon-48.png', 10, 8, 33)
        #self.set_font('Arial', 'B', 15)

        #self.cell(80)

        #self.cell(30, 10, 'UniCloud', 1, 0, 'c')

        self.ln(5)

    
    def footer(self):

        e_width = self.w - 2*self.l_margin
        
        self.set_y(-10)
        self.set_font('Arial', 'I', 8)
        self.cell(e_width/2, 10, 'Page ' + str(self.page_no()), 0, 0, 'r')

        self.set_text_color(255,255,0)
        self.cell(e_width/2, 10, '@UniCloud', 0, 0, 'r')



if __name__ == '__main__':

#    from fpdf import FPDF

#    pdf=FPDF()
    pdf=UniCloudPdf()

    #make an instance of the Template class
    pdf_temp = Templates(pdf_cls=pdf)

    # Example performs each of the template with title and without title
    pdf_temp.template3(title='UniCloud Test Pdf', author='Avour')

    pdf_temp.template1(title='UniCloud Test Pdf', body=loremipsum_2*2)
    pdf_temp.template1(body=loremipsum_2*2)
    pdf_temp.template2(title='UniCloud Test Pdf', body_1=loremipsum_1*2, body_2=loremipsum_2*3)
    pdf_temp.template2(body_1=loremipsum_1*2, body_2=loremipsum_2*3)

    pdf.output('UnicloudPdf.pdf')