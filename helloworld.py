import urllib, re

    
def buscaPagina(strUrl):
    sock = urllib.urlopen(strUrl)
    htmlSource = sock.read()
    sock.close()
    return htmlSource
    
def parseJogador(pagesource,arquivo):
    
    listaScouts = ['Time','Nome','Posicao','rodada','atleta_jogou','pontos_ult','pontos_media','preco','preco_variacao','confronto','mando','FS_rodada','A_rodada','FT_rodada','FD_rodada','FF_rodada','G_rodada','RB_rodada','SG_rodada','DD_rodada','DP_rodada','PE_rodada','I_rodada','PP_rodada','FC_rodada','GC_rodada','CA_rodada','CV_rodada','GS_rodada']
    
    jogadorDict = {}
    scoutDict = {}
    
    nomeJogador = buscaNome.search(pagesource).group(1)
    timeJogador = buscaTime.search(pagesource).group(1)
    posJogador = buscaPos.search(pagesource).group(1)
    
    colsenc = buscaCol.finditer(pagesource)
    rowsenc = buscaLinha.finditer(pagesource)
    
    header = "Time,Nome,Posicao,"
    
    for m in colsenc:
        header += m.group(1).split(',')[2]
        header += ","
    
    header = header[0:len(header)-1]
    hList = header.split(',')
    
    for n in rowsenc:
        
        rodadaDict = {}
        
        line = timeJogador + "," + nomeJogador + "," + posJogador + ","
        line += n.group(1).replace("{v:0,f:'-'}","0.00")
        
        lList = line.split(',')
        
        for x in range (0, len(hList)):
            chave = hList[x].replace("'","")
            valor = lList[x].replace("'","")
            rodadaDict[chave] = valor
        
        arquivo.write("<tr>")
        
        for scout in listaScouts:
            
            valorScout = ""
            
            try:
                valorScout = rodadaDict[scout]
            except Exception, e:
                valorScout = "0.00"
            
            if scout <> "rodada":
                valorScout = valorScout.replace(".",",")
            
            arquivo.write("<td>" + valorScout + "</td>")
            
        arquivo.write("</tr>")


def imprimeCabecalho(arquivo):
    strpagina = """\
<!DOCTYPE html>
<html>
<head> <meta charset="utf-8" />
<title> Extra&ccedil;&atilde;o de Scouts Cartola</title>
<body>
<table border = 2>
<thead>
<tr>
<th>Time</th>
<th>Nome</th>
<th>Posicao</th>
<th>Rodada</th>
<th>Jogou</th>
<th>Pontos</th>
<th>Pontos M&eacute;dia</th>
<th>Pre&ccedil;o</th>
<th>Pre&ccedil;o Varia&ccedil;&atilde;o</th>
<th>Confronto</th>
<th>Mando</th>
<th>FS</th>
<th>A</th>
<th>FT</th>
<th>FD</th>
<th>FF</th>
<th>G</th>
<th>RB</th>
<th>SG</th>
<th>DD</th>
<th>DP</th>
<th>PE</th>
<th>I</th>
<th>PP</th>
<th>FC</th>
<th>GC</th>
<th>CA</th>
<th>CV</th>
<th>GS</th>
</tr>
</thead>
<tbody>
"""
    arquivo.write(strpagina)

def imprimeRodape(arquivo):
    strpagina = """\
</tbody>
</table>
</body>
</head>
</html>
"""
    arquivo.write(strpagina)
            

buscaNome = re.compile(r'<a href=\"\/jogador\/.*?\">(.*?)<\/a>')
buscaPos = re.compile(r'<a href=\"\/posicao\/.*?\" itemprop=\"jobTitle\">(.*?)</a>')
buscaTime = re.compile(r'<a href=\"\/clube\/.*?\" itemprop=\"worksFor\".*?>(.*?)</a>')
buscaCol = re.compile(r'data\.addColumn\((.*?)\)')
buscaLinha = re.compile(r'data\.addRow\(\[(.*?)\]\)')    
buscaListaJogadores = re.compile(r'<a href=\"(\/jogador\/.*?\/[0-9]*?)\"')


if __name__ == '__main__':
    
    paginaJogadores = buscaPagina("http://www.scoutscartola.com/jogador")
    
    jogenc = buscaListaJogadores.finditer(paginaJogadores)
    
    ListaJogadores = []
    
    for m in jogenc:
        ListaJogadores.append("http://www.scoutscartola.com" + m.group(1))
        
    setJogadores = set(ListaJogadores)
    ListaJogadores = list(setJogadores)
    
    #ListaJogadores = ["http://www.scoutscartola.com/jogador/rogerio-ceni/38055","http://www.scoutscartola.com/jogador/lucas-pratto/73649","http://www.scoutscartola.com/jogador/leandro/38071"]
    
    with open ("ExtracaoScouts.html","w") as text_file:
        imprimeCabecalho(text_file)
        
        for x in ListaJogadores:
            pagesource = buscaPagina(x)
            scoutsJogador = parseJogador(pagesource,text_file)
        
        imprimeRodape(text_file)
  
        
        
    
    
    
    
         
    
    

    