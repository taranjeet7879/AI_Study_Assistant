const fileInput =
document.getElementById("pdfFile");

fileInput.addEventListener(
"change",
() => {

const file = fileInput.files[0];

if(file){

document.getElementById(
"fileName"
).innerText = file.name;

}
}
);

function showLoader(){

document.getElementById(
"loader"
).style.display="block";
}

function hideLoader(){

document.getElementById(
"loader"
).style.display="none";
}

async function uploadPDF(){

const file = fileInput.files[0];

if(!file){

alert("Select PDF first");

return;
}

const formData = new FormData();

formData.append(
"pdf",
file
);

showLoader();

const response =
await fetch(
"/upload",
{
method:"POST",
body:formData
}
);

const data =
await response.json();

hideLoader();

if(data.success){

document.getElementById(
"statusCard"
).classList.remove(
"hidden"
);

document.getElementById(
"loadedFileName"
).innerText =
file.name;

document.getElementById(
"output"
).innerText =
"PDF uploaded successfully.";

}else{

alert(data.message);
}
}

async function callRoute(route){

showLoader();

const response =
await fetch(route,{
method:"POST"
});

const data =
await response.json();

hideLoader();

document.getElementById(
"output"
).innerText =
data.result;
}

function generateSummary(){
callRoute("/summary");
}

function generateQuestions(){
callRoute("/questions");
}

function generateMCQs(){
callRoute("/mcqs");
}

function generateRevision(){
callRoute("/revision");
}

async function askQuestion(){

const question =
document.getElementById(
"question"
).value;

if(!question){

alert(
"Enter a question"
);

return;
}

showLoader();

const response =
await fetch(
"/ask",
{
method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:JSON.stringify({
question:question
})
}
);

const data =
await response.json();

hideLoader();

document.getElementById(
"output"
).innerText =
data.answer;
}