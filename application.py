from flask import Flask, render_template, request, redirect, url_for
import pyodbc
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def conexao():
	server = 'faisp.database.windows.net'
	database = 'FAISP'
	username = 'luigi'
	password = 'Senha1234!@#$'
	driver= '{ODBC Driver 17 for SQL Server}'
	cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
	return cnxn.cursor()
   

@app.route('/novo')
def novo():
   return render_template('formulario.html')

@app.route('/')
def listar():

   cursor = conexao()

   cursor.execute("SELECT * FROM alunoFaisp ORDER BY id")
   result_set = cursor.fetchall()

   strHtml = '<!DOCTYPE html> '
   strHtml += '<html> '
   strHtml += '<body> '

   strHtml += '<table border="1"> '
   strHtml += '<tr> '
   strHtml += '<th>Nome</th> '
   strHtml += '<th>Email</th> '
   strHtml += '<th>link</th> '
   strHtml += '</tr> '
   

   for row in result_set:
      strHtml += '<tr> '
      strHtml += '<td>'+row.nome+'</td> '
      strHtml += '<td>'+row.email+'</td> '
      strHtml += '<td><a href="https://webappwinflask.azurewebsites.net/excluir/'+str(row.id)+'">Excluir</a></td> '
      strHtml += '</tr> '
   
   
   strHtml += '</table> '
   strHtml += '<p><a href="https://webappwinflask.azurewebsites.net/novo">Cadastrar Novo Aluno</a></p> '
   strHtml += '</body> '
   strHtml += '</html> '
   
   return strHtml   

@app.route('/resultado',methods = ['POST', 'GET'])
def resultado():
   if request.method == 'POST':
      result = request.form
      name=request.form['Name']
      email=request.form['Email']

      cursor = conexao()

      sql  = "INSERT INTO alunoFaisp VALUES ('{}','{}')".format(name,email)
      
      cursor.execute(sql)
      cursor.commit()
      cursor.close()
      #return "Usuário Inserido com sucesso " + name
      return redirect(url_for('listar'))

@app.route('/excluir/<idUsr>')
def excluir(idUsr):
   
   cursor = conexao()

   sql  = "DELETE FROM alunoFaisp where id ={}".format(idUsr)

   cursor.execute(sql)
   cursor.commit()
   cursor.close()
   return redirect(url_for('listar'))
      
if __name__ == '__main__':
    app.run()
