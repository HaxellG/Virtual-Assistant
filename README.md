Descripción:
Este código en Python define un asistente de voz llamado "Sara". Este asistente puede realizar una variedad de tareas, 
incluyendo reconocimiento de voz, habla, búsqueda en Wikipedia, contar chistes, abrir sitios web, reproducir videos en 
YouTube e interactuar de manera conversacional utilizando la biblioteca de Python Chatterbot.

Dependencias:
Se necesitan las siguientes bibliotecas de Python para ejecutar este código:

speech_recognition
pyttsx3
pywhatkit
datetime
wikipedia
pyjokes
json
webbrowser
automatic
time
chatterbot
tu módulo personalizado database

Uso:
Este código escucha continuamente los comandos de voz del usuario y realiza acciones basadas en estos comandos. 
Aquí están los comandos que entiende:

"hablar" - Sara entra en un modo conversacional y chatea con el usuario.
"me escuchas" - Sara confirma si puede escuchar al usuario.
"reproduce" - Sara reproduce un video en YouTube. El video a reproducir debe especificarse después del comando "reproduce".
"hora" - Sara dice la hora actual.
"busca" - Sara busca en Wikipedia un término. El término a buscar debe especificarse después del comando "busca".
"chiste" - Sara cuenta un chiste.
"repite" - Sara repite lo que el usuario dice después del comando "repite".
"abre" - Sara abre ciertos sitios web. Los sitios web compatibles son "youtube", "mercadolibre", "google", 
"netflix" y "whatsapp" (ten en cuenta que puedes añadir cualquier otro que desees).
"desconectar" - Sara se apaga.

Ten en cuenta que Sara solo responde a los comandos cuando escucha su nombre mencionado en el comando. Además, 
esta versión del asistente virtual solo entiende comandos en español.

Por favor, reemplaza el módulo database con tu propio módulo que defina una función get_questions_answers(). 
Esta función debería devolver una lista de pares de preguntas y respuestas utilizadas para entrenar el Chatterbot.
