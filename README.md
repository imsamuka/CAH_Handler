# CardsAgainstHumanity Handler

This is a system write in Python 3 to handle custom *Cards Against Humanity* decks. The [CAH_Database.py](https://github.com/imsamuka/CAH_Handler/blob/master/CAH_PDF-Generator.py) reads a `.txt` file formatted as following:

TXT IMAGE

It generates 2 lists, one containing all the white cards and the other, the black cards.

For the time being we can use these lists for 2 purposes:

 - [CAH_TXT-Generator.py](https://github.com/imsamuka/CAH_Handler/blob/master/CAH_TXT-Generator.py "CAH_TXT-Generator.py") can use it to generate another `.txt` formatted.
 - [CAH_PDF-Generator.py](https://github.com/imsamuka/CAH_Handler/blob/master/CAH_PDF-Generator.py "CAH_PDF-Generator.py") can use it to generate a `.pdf` containing all you need to print your custom deck.

PDF IMAGE

**In the future**, i will rewrite a code that generates the `.png` files to use in *Table Top Simulator* ~~which for some reason, i wrote in Java~~. These cards will look like that:

The [res](https://github.com/imsamuka/CAH_Handler/tree/master/res "res") folder contain the [DEFAULTCARDS_PT-BR.txt](https://github.com/imsamuka/CAH_Handler/blob/master/res/DEFAULTCARDS_PT-BR.txt "DEFAULTCARDS_PT-BR.txt") which are the standard game cards in Brazilian Portuguese.
