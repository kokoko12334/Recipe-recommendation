
function createRecipeCard(recipe, extractedValues) {
    var card = $('<div>').addClass('col-12 col-md-6 col-lg-3 my-3');
    var cardInner = $('<div>').addClass('card h-100').css("max_width", "20rem").css("border-radius", "15px").css("height", "100%");;
    var cardImg = $('<img>').addClass('card-img-top').attr('alt', 'Recipe Image').css('object-fit', 'cover').css('height', '25%');

    cardImg.attr('src', recipe.image_url);
    cardImg.on('error', function () {
        console.error("이미지 로드에 실패했습니다.:", recipe.image_url);
        $(this).attr('src', '/static/no_image.jpg'); // 이미지 로드 실패 시 대체할 이미지의 경로를 설정

    });

    var cardBody = $('<div>').addClass('card-body d-flex flex-column');
    var cardTitle = $('<h5>').addClass('card-title').text(recipe.recipe_name);
    var cardText = $('<p>').addClass('card-text').css('flex-grow', '1');

    // ingre_str = recipe.ingre.slice(1, -1).trim();
    // var ingreArray = ingre_str.split(","); // 재료 배열로 분할
    var ingreArray = recipe.preprocessed_ingredients.map(item => item.ingredient);
    ingreArray.forEach(function (ingreItem) {
        var ingre_string = ingreItem.trim().replaceAll('\'', '')
        var ingreElement = $('<span>').text(ingre_string).addClass('lightext'); // 재료 항목 생성
        if (input_set.has(ingre_string)) {
            ingreElement.css("background", "linear-gradient(to top, #bfffa1 100%, transparent 40%)"); // 레시피 재료와 일치하는 경우 굵은 글씨로 설정
        }
        cardText.append(ingreElement).append(' '); // 재료 항목 추가
    });



    var cardserving = $('<p>').text(recipe.serving).css('align-self', 'flex-end').css('margin-bottom', '0');
    var cardLink = $('<a>').addClass('btn btn-primary mt-auto').attr('href', recipe.url).text('레시피 링크').css('align-self', 'flex-end');

    cardBody.append(cardTitle, cardText, cardserving, cardLink);
    cardInner.append(cardImg, cardBody);
    card.append(cardInner);

    return card;
}

function adjustFooterPosition() {
    var contentHeight = $('body').height(); // 페이지 내용의 높이
    var windowHeight = $(window).height(); // 브라우저 창의 높이
    var footerHeight = $('.footer').outerHeight(); // 푸터의 높이

    if (contentHeight + footerHeight < windowHeight) {
        $('.footer').css({
            position: 'fixed',
            bottom: 0
        });
    } else {
        $('.footer').css({
            position: 'static' // 페이지 내용이 푸터를 가릴 때는 푸터를 일반적인 위치로 표시
        });
    }
}

$(document).ready(function () {

    var input = document.querySelector('input[name=ingredients]');
    var rangeBar = document.querySelector('.range');
    var tagify = new Tagify(input, {
        whitelist: ingre_data,
        enforceWhitelist: true,
        editTags: false,
        dropdown: {
            classname: "color-blue",
            enabled: 0,              // show the dropdown immediately on focus
            maxItems: 10,
            position: "text",         // place the dropdown near the typed text
            closeOnSelect: false,          // keep the dropdown open after selecting a suggestion
            highlightFirst: true,
        },

    });

    tagify.on('add', function (e) {

        var tagText = e.detail.data.value; // 추가된 태그의 텍스트
        var tagId = 'tag-' + tagText.replace(/\s+/g, '-').toLowerCase(); // 공백을 '-'로 대체하고 소문자로 변환하여 ID 생성
        var container = document.createElement('div');
        container.className = 'tag-range-container';
        container.id = tagId; // 고유 ID 설정

        var label = document.createElement('span');
        label.className = 'label';
        label.textContent = tagText;

        var rangeInput = document.createElement('input');
        rangeInput.type = 'range';
        rangeInput.name = 'points';
        rangeInput.min = '0';
        rangeInput.max = '5';
        rangeInput.step = '0.1';

        var rangeValue = document.createElement('span');
        rangeValue.className = 'range-value';
        rangeValue.textContent = '1.0';

        rangeInput.addEventListener('input', function () {
            var value = parseFloat(rangeInput.value);
            var displayValue = 0.5 + (value / 10);
            rangeValue.textContent = displayValue.toFixed(1);
        });

        container.appendChild(label);
        container.appendChild(rangeInput);
        container.appendChild(rangeValue);
        rangeBar.appendChild(container);
    });

    // 태그가 삭제될 때 관련 요소도 삭제
    tagify.on('remove', function (e) {
        var tagText = e.detail.data.value;
        var tagId = 'tag-' + tagText.replace(/\s+/g, '-').toLowerCase();
        var container = document.getElementById(tagId);
        if (container) {
            container.parentNode.removeChild(container);
        }
    });

    document.getElementById('ingre').addEventListener('submit', function (event) {
        event.preventDefault(); // 기본 제출 동작 방지

        var formData = new FormData(this); // 폼 데이터 생성

        var outputData = [];

        for (var pair of formData.entries()) {
            if (pair[0] === 'ingredients') {
                if (!pair[1]) {
                    alert('입력칸이 비었습니다.');
                    return;
                }

                try {
                    var tags = JSON.parse(pair[1]);
                    tags.forEach(tag => {
                        var tagId = 'tag-' + tag.value.replace(/\s+/g, '-').toLowerCase();
                        var container = document.getElementById(tagId);
                        if (container) {
                            var rangeValue = container.querySelector('.range-value').textContent;
                            outputData.push({ values: tag.value, range: parseFloat(rangeValue) });
                        }
                    });
                } catch (e) {
                    alert('Invalid JSON input for ingredients.');
                    return;
                }
            }
        }
        var loader = document.querySelector('.loader');
        loader.style.display = 'block';
        fetch('/recipes/recipe_rec/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(outputData),
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).then(data => {
            // console.log('Success:', data);
            // var cardRow = $('#cardRow');
            var cardRow = $('#cardRow');
            cardRow.empty(); // 기존 카드 모두 제거
            var footer = document.querySelector(".footer");
            footer.style.position = "fixed";
            var recipes = data.data;
            console.log(data);
            console.log(recipes);
            var ingredientsInput = document.getElementById('ingredients');
            var ingredientsValue = ingredientsInput.value;

            // JSON 문자열을 JavaScript 객체로 파싱
            var parsedValue = JSON.parse(ingredientsValue);

            // "value" 키의 값만을 추출하여 새로운 배열에 저장
            var extractedValues = parsedValue.map(function (item) {
                return item.value;
            });
            input_set = new Set(extractedValues)

            loader.style.display = 'none';


            const jsonString = "['어묵', '김밥용김', '당면', '양파', '당근', '깻잎', '튀김가루', '올리브유', '간장', '참기름']";

            // 주어진 문자열의 작은따옴표를 큰따옴표로 변경
            const correctedJsonString = jsonString.replace(/'/g, '"');
            const array = JSON.parse(correctedJsonString);
            // console.log(array);
            for (let i = 0; i < recipes.length; i++) {

                var card = createRecipeCard(recipes[i], input_set);
                cardRow.append(card);
            }
            adjustFooterPosition();

        })
            .catch(error => {
                console.error('Error:', error);
            });
    });

});
