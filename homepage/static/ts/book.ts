declare var ParallaxHook: any


document.addEventListener('DOMContentLoaded', async () => {
    const container = <HTMLDivElement>
        document.getElementById('book-app')
    new ParallaxHook(
        container,
        () => {},
        (progress: any) => {
            container.style.opacity = `${Math.min(1, progress.value * 3)}`;
            container.style.transform = `translateY(${10 - (progress.value * 20)}rem)`
        },
        () => {}
    ).attach()
})
