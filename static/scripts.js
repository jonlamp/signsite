function getRandomInt(min,max){
    return Math.floor(Math.random() * (max-min) + min);
}
function getSignData(){
    const signs = ["Capricorn","Aquarius","Pisces","Aries","Taurus","Gemini",
        "Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius"];
    return getRandomData(signs,1000);    
}
function getPersonalityData(){
    const personalities=[
        "ESTJ", "ENTJ", "ESFJ", "ENFJ", 
        "ISTJ", "ISFJ", "INTJ", "INFJ", 
        "ESTP", "ESFP", "ENTP", "ENFP", 
        "ISTP", "ISFP", "INTP", "INFP"
    ]
    return getRandomData(personalities,1000);
}
function getSignPersonalityDataTest(){
    let results = [];
    let id = 0;
    const signs = [
        "Capricorn","Aquarius","Pisces","Aries",
        "Taurus","Gemini","Cancer","Leo",
        "Virgo","Libra","Scorpio","Sagittarius"];
    const personalities=[
        "ESTJ", "ENTJ", "ESFJ", "ENFJ", 
        "ISTJ", "ISFJ", "INTJ", "INFJ", 
        "ESTP", "ESFP", "ENTP", "ENFP", 
        "ISTP", "ISFP", "INTP", "INFP"
    ];
    signs.forEach(s => {
        personalities.forEach(p => {
            id += 1
            results.push({
                'id':id,
                'sign':s,
                'mbti':p,
                'total': getRandomInt(1,100)
            });
        });
    });
    return results;
}
function getRandomData(labels, maxCount){
    let response = {};
    labels.forEach(lbl => {
        let rand = getRandomInt(1,maxCount);
        response[lbl] = rand;
    });
    return response;
}
function generateBarChart(data, target, active){
    $(target).html("");
    let total = 0;
    let max = 0;
    Object.keys(data).forEach(label =>{
        total += data[label];
        max = Math.max(data[label], max)
    });
    Object.keys(data)
        .sort()
        .forEach(label=>{
            //let width = Math.round((data[label]/total)*100)*3;
            let width = Math.round((data[label]/max)*100)/1.5;
            let newData = $("<div>").html("")
            newData.attr('class','data-group');
            let chartLabel = $("<div>").text(label);
            chartLabel.attr('class','label');
            newData.append(chartLabel)
            let bar = $('<div>').html("");
            bar.attr('class','chart-item');
            bar.attr('style','width:' + width.toString()+"%");
            if(label.toLowerCase() === active.toLowerCase()){
                bar.attr('class', 'chart-item active');
            }
            newData.append(bar);
            $(target).append(newData);
            let number = $('<div>').html(data[label].toString());
            newData.append(number);            
        })
};
function init(data, userSign, userMBTI){
    /*expects data to be an array of objects containing:
        -id
        -sign
        -mbti
        -total (count of values from DB for particular combination)
    */
    const signs = {
        "capricorn":0,"aquarius":0,"pisces":0,"aries":0,
        "taurus":0,"gemini":0,"cancer":0,"leo":0,
        "virgo":0,"libra":0,"scorpio":0,"sagittarius":0
    }
    const personalities={
        "ESTJ":0, "ENTJ":0, "ESFJ":0, "ENFJ":0, 
        "ISTJ":0, "ISFJ":0, "INTJ":0, "INFJ":0, 
        "ESTP":0, "ESFP":0, "ENTP":0, "ENFP":0, 
        "ISTP":0, "ISFP":0, "INTP":0, "INFP":0
    };
    data.forEach(i => {
        signs[i['sign']] += i['total'];
        personalities[i['mbti']] += i['total'];
    })
    $(".sign").text(userSign);
    $(".mbti").text(userMBTI);
    console.log(signs);
    generateBarChart(signs,"#sign-bargraph .chart",userSign);
    generateBarChart(personalities,'#mbti-bargraph .chart',userMBTI);
    return data;
}
