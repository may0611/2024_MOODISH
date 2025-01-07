import React, { useState } from 'react';
import { View, Text, Button, TextInput } from 'react-native';

export default function App() {
  const [apiResult, setApiResult] = useState(null); // API 결과를 저장할 상태
  const [inputText, setInputText] = useState('');
  const [inputText_time, setInputText_time] = useState(''); 
  const [inputText_diffi, setInputText_diffi] = useState(''); 
  const [isButtonDisabled, setIsButtonDisabled] = useState(false); // 버튼 비활성화 상태 관리

  const handleTextChange = (text) => {
    setInputText(text);
  };

  const handleTextChange_time = (text) => {
    setInputText_time(text);
  };

  const handleTextChange_diffucult = (text) => {
    setInputText_diffi(text);
  };

  // 감정 분석
  const callApi_emo = async () => {
    setIsButtonDisabled(true);
    try {
      const response = await fetch('http://172.25.86.64:5000/emotion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({

          // image형태 (아마 base64)

        }),
      });

      const result = await response.json();
      setIsButtonDisabled(false);
      setApiResult(result.result); // Flask 서버에서 반환한 'result' 값을 상태에 저장
      // 변수 이름 다르게 해야 함
    } catch (error) {
      console.error('Error calling API:', error);
    }
  };


  // 추천 시스템
  const callApi_rec = async () => {
    setIsButtonDisabled(true);
    try {
      const response = await fetch('http://172.25.86.64:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userInput: inputText, // 사용자가 입력한 텍스트
          userInput_time: inputText_time,
          userInput_diffi: inputText_diffi,
        }),
      });
      const result = await response.json();
      setIsButtonDisabled(false);
      setApiResult(result.result); // Flask 서버에서 반환한 'result' 값을 상태에 저장
  
    } catch (error) {
      console.error('Error calling API:', error);
    }
  };

  const resultLines = apiResult ? apiResult.split('|') : [];

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>
        재료: 
      </Text>
      <TextInput
        style={{
          height: 40,
          borderColor: 'gray',
          borderWidth: 1,
          marginBottom: 20,
          width: '100%',
          paddingHorizontal: 10,
        }}
        placeholder="재료를 입력하세요"
        value={inputText}
        onChangeText={handleTextChange}
      />
      <Text>
          시간: ,
      </Text>
      <TextInput
        style={{
          height: 40,
          borderColor: 'gray',
          borderWidth: 1,
          marginBottom: 20,
          width: '100%',
          paddingHorizontal: 10,
        }}
        placeholder="시간을 입력하세요 (최소 5)"
        value={inputText_time}
        onChangeText={handleTextChange_time}
      />
      <Text>
          난이도:,
          </Text>
          <TextInput
        style={{
          height: 40,
          borderColor: 'gray',
          borderWidth: 1,
          marginBottom: 20,
          width: '100%',
          paddingHorizontal: 10,
        }}
        placeholder="초급 중급 고급 아무나 중 선택"
        value={inputText_diffi}
        onChangeText={handleTextChange_diffucult}
      />
          <Text>
          happy: 1,
          </Text>
          <Text>
          board: 0,
          </Text>
          <Text>
          tired: 0,
          </Text>
          <Text>
          stress: 0,
          </Text>
          <Text>
          sad: 0
      </Text>


      <Button title="Recommend" onPress={callApi_rec} disabled={isButtonDisabled}/>
      
      <Text>
        Your Recommend :
      </Text>

      {resultLines.map((line, index) => (
        <Text key={index}>{line}</Text>
      ))}

    </View>
  );
}