import datetime
from django.db import models
from django.utils import timezone

def rewrite_mpolynomial(mpolynomial):
    sign_list = []
    for i in range(2,10):
        sign_list.append("^"+ str(i))
    b = ""
    for i in range(len(mpolynomial)):
        if mpolynomial[i] == "-" or mpolynomial[i] == "+":
            # if possible there is x^n or y^n before this sign (n number)
            if i > 2:
                # if sign is before ^n
                if mpolynomial[i-2]+ mpolynomial[i-1] in sign_list:
                    b = b + " " + mpolynomial[i] + " "
                # sign is in m_ij
                else:
                    b= b + mpolynomial[i]
            # sign is in m_ij
            else:
                b = b + mpolynomial[i]
        elif mpolynomial[i] == "x" or mpolynomial[i] == "y":
            b = b + " " + mpolynomial[i]
        # elif wq[i] == " ":  # naceloma to ni mozno ker smo nardil replace (wq)
        #     b = b
        else:
            b = b + mpolynomial[i]
    if b[0] == " ":
        b = b[1:len(b)]
    if b[len(b)-1] == " ":
        b == b[0:len(b) - 1]
    return b




# Create your models here. # preimenuj polynom
class Mpolynom(models.Model):
    mpolynomyal = models.CharField("M-polynomial", max_length=1000) ### popravi, zaradi presledkov ne dela
    structure_name = models.CharField(max_length=200, unique=True) # keywords - glede na to da unique?? dopuscamo vec ali ne
    #structure_picture = models.ImageField()
    keywords = models.CharField(max_length=200) #
    comments = models.TextField(blank=True)
    references = models.TextField(blank=True)
    links = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now=True) #spremeni primere
   # class Foo(models.Model):
    nb_tokens = models.PositiveSmallIntegerField(default=0)
    def save(self, *args, **kwargs):
        b = rewrite_mpolynomial(self.mpolynomyal)
        split = b.split()
        self.nb_tokens = len(split)
        super(Mpolynom, self).save(*args, **kwargs) # Call the "real" save() method.
    # omogoci iteracijo
    def __iter__(self):
       ''' Returns the Iterator object '''
       return iter(self.mpolynomyal)
    def __str__(self):
        return self.mpolynomyal #tukaj poves reprezentacijo objektov
        #dodamo metodo, ki deluje na teh objektih
    def published_recently(self): 
        """true if published in last seven days"""
        return self.publication_date >= timezone.now().date() - datetime.timedelta(days=7)
    # change name displayed on django admin site
    class Meta:
        verbose_name = "M-polynomial"