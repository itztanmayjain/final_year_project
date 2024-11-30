const bars = document.querySelector(".bar"),
close = document.querySelector(".close"),
menu = document.querySelector(".menu");

bars.addEventListener("click", () => {
    menu.classList.add("active");
    gsap.from(".menu", {
        opacity: 0,
        duration: .3
    })

    gsap.from(".menu ul", {
        opacity: 0,
        x: -300
    })
});

close.addEventListener("click", () => {
    menu.classList.remove("active")
});

function animateContent(selector) {
    selector.forEach((selector) => {
        gsap.to(selector, {
            y: 30,
            duration: 0.1,
            opacity: 1,
            delay: 0.2,
            stagger: 0.2,
            ease: "power2.out",
        });
    });
}

function scrollTirggerAnimation(triggerSelector, boxSelectors) {
    const timeline = gsap.timeline({
        scrollTrigger: {
            trigger: triggerSelector,
            start: "top 50%",
            end: "top 80%",
            scrub: 1,
        },
    });

    boxSelectors.forEach((boxSelector) => {
        timeline.to(boxSelector, {
            y: 0,
            duration: 1,
            opacity: 1,
        });
    })
}

function swipeAnimation(triggerSelector, boxSelectors) {
    const timeline = gsap.timeline({
        scrollTrigger: {
            trigger: triggerSelector,
            start: "top 50%",
            end: "top 100%",
            scrub: 3,
        },
    });

    boxSelectors.forEach((boxSelector) => {
        timeline.to(boxSelector, {
            x: 0,
            duration: 1,
            opacity:1,
        });
    });
}

function galleryAnimation(triggerSelector, boxSelectors) {
    const timeline = gsap.timeline({
        scrollTrigger: {
            trigger: triggerSelector,
            start: "top 100%",
            end: "bottom 100%",
            scrub: 1,
        },
    });

    boxSelectors.forEach((boxSelector) => {
        timeline.to(boxSelector, {
            y: 0,
            opacity: 1,
            duration: 1,
        });
    });
}




animateContent([".home .content h5, .home .content h1, .home .content p, .home .content .search"]);

scrollTirggerAnimation(".info", [".info .box1", ".info .box2", ".info .box3"]);

scrollTirggerAnimation(".feedback .container", [".feedback .label", ".feedback .heading", ".feedback .paragraph"]);


swipeAnimation(".product", [".product .heading", ".product .content"])


galleryAnimation(".product .gallery", [".product .gallery .box1",".product .gallery .box2",".product .gallery .box3",".product .gallery .box4",".product .gallery .box5"])

galleryAnimation(".featured .gallery", [".featured .gallery .box1",".featured .gallery .box2",".featured .gallery .box3",".featured .gallery .box4"])

galleryAnimation(".feedback .voices", [".feedback .voices .box1",".feedback .voices .box2",".feedback .voices .box3",".feedback .voices .box4",".feedback .voices .box5",".feedback .voices .box6"])

