import React, { useEffect, useState } from 'react';
import { View, Text, Linking, Image, TouchableOpacity, StyleSheet, Modal } from 'react-native';

const RecipeDetail = ({ navigation, route }) => {
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [apiResult, setApiResult] = useState(null); // API 결과를 저장할 상태


    const { result_name } = route.params;

        //이미지 불러오기
        useEffect(() => {
        const callApi_img = async () => {
            try {
              const response = await fetch('http://172.25.81.103:5000/foodImg', { //위치에 따라 ip변경 필요
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  foodName: result_name,
                }),
              });
              const result = await response.json();
              setApiResult(result.img_link); // Flask 서버에서 반환한 'result' 값을 상태에 저장
        
            } catch (error) {
              console.error('Error calling API:', error);
            } finally {
          }
          };

          callApi_img();
        }, [result_name]);
    

    const handleYes = () => {
        navigation.navigate('Profile'); 
    };

    const handleNo = () => {
        navigation.navigate('Profile');  
    };

    const handleRecipe = () => {
        // 레시피 화면으로 이동
        const recipeLink = 'https://www.10000recipe.com/recipe/list.html?q=' + encodeURIComponent(result_name);
        Linking.openURL(recipeLink);
    };

    const handleYouTube = () => {
        // 유튜브 링크를 열기 위한 로직 추가
        const youtubeLink = 'https://www.youtube.com/results?search_query=' + encodeURIComponent(result_name) ;
        Linking.openURL(youtubeLink);
    };

    return (
        <View style={styles.container}>
            {apiResult ? (
                <Image source={{ uri: apiResult }} style={{ width: 300, height: 300 }} />
            ) : (
                <Text>이미지를 불러오는 중...</Text>
            )}
            <Text style={styles.title}> {result_name} </Text>

            <View style={styles.buttonContainer}>
                <TouchableOpacity style={styles.recipeButton} onPress={handleRecipe}>
                    <Text style={styles.buttonText}>레시피</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.youtubeButton} onPress={handleYouTube}>
                    <Text style={styles.buttonText}>유튜브</Text>
                </TouchableOpacity>
            </View>

            {showConfirmation && (
                <Modal
                    transparent={true}
                    animationType="fade"
                    visible={showConfirmation}
                >
                    <View style={styles.modalOverlay}>
                        <View style={styles.modalContent}>
                            <Text style={styles.modalTitle}>추천 레시피가{'\n'} 마음에 들었나요?</Text>
                            <View style={styles.modalButtonContainer}>
                                <TouchableOpacity style={styles.modalButton1} onPress={handleYes}>
                                    <Text style={styles.buttonText}>네</Text>
                                </TouchableOpacity>
                                <TouchableOpacity style={styles.modalButton2} onPress={handleNo}>
                                    <Text style={styles.buttonText}>아니요</Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View>
                </Modal>
            )}

            {/* 하단 네비게이션 바 */}
            <View style={styles.navBar}>
                <TouchableOpacity onPress={() => navigation.navigate('Search')}>
                    <Image source={require('./assets/reading glasses.png')} style={styles.navIcon1} />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => navigation.navigate('Profile')}>
                    <Image source={require('./assets/home.png')} style={styles.navIcon} />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => navigation.navigate('Save')}>
                    <Image source={require('./assets/refrigerator.png')} style={styles.navIcon1} />
                </TouchableOpacity>
                <TouchableOpacity onPress={() => navigation.navigate('MyPage')}>
                    <Image source={require('./assets/userIcon.png')} style={styles.navIcon} />
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#fff',
    },
    image: {
        width: 200,
        height: 200,
        marginBottom: 20,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    buttonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        width: '90%',
        marginTop: 40,
    },
    recipeButton: {
        backgroundColor: '#6C95F0',
        padding: 15,
        borderRadius: 5,
        flex: 1,
        marginRight: 10,
        alignItems: 'center',
    },
    youtubeButton: {
        backgroundColor: '#FD7D7D',
        padding: 15,
        borderRadius: 5,
        flex: 1,
        marginLeft: 10,
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        width: '80%',
        backgroundColor: '#fff',
        borderRadius: 10,
        padding: 20,
        alignItems: 'center',
    },
    modalTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 20,
    },
    modalButtonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        width: '100%',
    },
    modalButton1: {
        flex: 1,
        backgroundColor: '#6C95F0',
        padding: 15,
        borderRadius: 5,
        marginHorizontal: 10,
        alignItems: 'center',
    },
    modalButton2: {
        flex: 1,
        backgroundColor: '#FD7D7D',
        padding: 15,
        borderRadius: 5,
        marginHorizontal: 10,
        alignItems: 'center',
    },
    navBar: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        backgroundColor: '#FFFFFF',
        borderTopWidth: 1,
        borderTopColor: '#E0E0E0',
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        paddingVertical: 10
    },
    navIcon: {
        width: 30,
        height: 30,
        resizeMode: 'contain',
    },
    navIcon1: {
        width: 20,
        height: 20,
        resizeMode: 'contain',
        marginTop: 5
    },
});

export default RecipeDetail;
