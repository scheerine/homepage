declare var anime: any;
declare var ParallaxHook: any

document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('blume-section')
    const bg = document.getElementById('blume-background')
    const treppe = document.getElementById('blume-treppe')
    const blume = document.getElementById('blume')
    new ParallaxHook(
        container,
        () => {},
        (progress: any) => {
            anime({
                targets: treppe,
                translateY: -(progress.value * 30),
                rotate: progress.value * 90,
                scale: 1 + 1.2 * progress.value,
                duration: 100,
            })
            anime({
                targets: blume,
                translateY: -(progress.value * 30),
                scale: 1 + 0.5 * progress.value,
                duration: 100,
            })
        },
        () => {}
    ).attach()
})
