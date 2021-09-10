declare var anime: any;
declare var ParallaxHook: any


document.addEventListener('DOMContentLoaded', async () => {
    const container = <HTMLDivElement>
        document.getElementById('book-app')
    new ParallaxHook(
        container,
        () => {},
        (progress: any) => {
            anime({
                targets: container,
                opacity: Math.min(1, progress.value * 3),
                translateY: 10 - (progress.value * 20),
                duration: 200,
            })
        },
        () => {}
    ).attach()
})
