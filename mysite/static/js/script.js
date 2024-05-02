
async function startStreaming() {
  try {
    const response = await fetch('/test');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    const reader = response.body.getReader();


    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log('Streaming complete');
        break;
      }
      // value는 Uint8Array 형식이므로 텍스트로 변환하여 출력합니다.
      const text = new TextDecoder().decode(value);
      console.log(text + '\n');

    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}


function startStreaming2() {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await fetch('/test');
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const reader = response.body.getReader();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          console.log('Streaming complete');
          resolve(); // 스트리밍 완료 후 프로미스를 성공으로 처리
          break;
        }
        // value는 Uint8Array 형식이므로 텍스트로 변환하여 출력합니다.
        const text = new TextDecoder().decode(value);
        console.log(text + '\n');
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      reject(error); // 오류가 발생하면 프로미스를 실패로 처리
    }
  });
}

document.getElementById('signInButton').addEventListener('click', function (event) {
  event.preventDefault(); // 기본 제출 동작 방지

  startStreaming2()
});



document.getElementById('anonymous').addEventListener('click', function () {
  fetch('/set_access/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ access: true })
  }).then(function (response) {
    window.location.href = '/recipe_page/';
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}