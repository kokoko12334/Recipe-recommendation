
$(document).ready(function () {

    var input = document.querySelector('input[name=ingredients]');

    var tagify = new Tagify(input, {
        whitelist: ingre_data,
        dropdown: {
            classname: "color-blue",
            enabled: 0,              // show the dropdown immediately on focus
            maxItems: 5,
            position: "text",         // place the dropdown near the typed text
            closeOnSelect: false,          // keep the dropdown open after selecting a suggestion
            highlightFirst: true,
            enforceWhitelist: true,
        }
    });

    document.getElementById('ingre').addEventListener('submit', function (event) {
        event.preventDefault(); // 기본 제출 동작 방지

        var formData = new FormData(this); // 폼 데이터 생성
        console.log(formData);
        fetch('/recipes/recipe_rec/', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // console.log('Success:', data);
                const container = document.getElementById('con');
                 
                const template = document.getElementById('recipeCardTemplate').content;
                template.innerHTML = '';
                var recipes = data.data;
                // console.log(recipes[0])
                for (let i = 0; i < 50; i++) {
                    const clone = document.importNode(template, true);
                    
                    clone.querySelector('.card-img-top').src = recipes[i].image_url;
                    clone.querySelector('.card-title').textContent = recipes[i].name;
                    clone.querySelector('.card-text').textContent = recipes[i].ingre;
                    clone.querySelector('p:nth-child(3)').textContent = `${recipes[i].serving}인분`;
                    clone.querySelector('.btn-primary').href = recipes[i].url;
                    container.appendChild(clone);

                    // 5의 배수마다 새로운 줄 추가
                    if ((i + 1) % 5 === 0) {
                        container.appendChild(document.createElement('br'));
                    }
                }

            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

});