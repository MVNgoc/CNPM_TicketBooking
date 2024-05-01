let collapseButton = document.getElementById('collapseButton');
let flightInfo = document.getElementById('flightInfo');
let iconUp = document.getElementById('iconUp')
let iconDown = document.getElementById('iconDown')

collapseButton.addEventListener('click', () => {
    if(flightInfo.classList.contains('animation_hidden')) {
        flightInfo.classList.remove('animation_hidden')
        flightInfo.classList.add('animation_show')
        if(iconDown.classList.contains('hidden')) {
            iconDown.classList.remove('hidden')
            iconUp.classList.add('hidden')
        }
    } else {
        flightInfo.classList.add('animation_hidden');
        flightInfo.classList.remove('animation_show');
        if(iconUp.classList.contains('hidden')) {
            iconUp.classList.remove('hidden')
            iconDown.classList.add('hidden')
        }
    }
});