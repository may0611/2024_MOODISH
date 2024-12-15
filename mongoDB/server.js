const express= require('express');
const app = express();

app.use(express.static(__dirname+'/public'))

const{MongoClient}=require('mongodb');

let db;
const url ='mongodb+srv://mayLEE:abcd@cluster0.1txw3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
new MongoClient(url).connect().then((client)=>{
    console.log('DB연결성공')
    db=client.db('moodish');
//3001 포트로 서버 연결해주세요 원하는 번호로 할 수 있음
    app.listen(3003, function(){

     console.log('listening on 3003')
});
}).catch((err)=>{
    console.log(err)
})

app.listen();


    app.get('/news',function(요청, 응답){//function 안 쓰고 (요청, 응답)=>이런 식으로도 사용 가능
       // db.collection('post').insertOne({title:'어쩌구'})
        
        });
        
  