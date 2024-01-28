function changePrices(selectedOption) {
    preco = selectedOption.getAttribute('data-preco');
    preco_promocional = selectedOption.getAttribute('data-preco-promocional');

    variation_preco.innerHTML = preco;
    variation_preco_promocional.innerHTML = ''
    variation_preco.classList.replace('product-old-price', 'product-price')
    variation_preco.classList.remove('text-muted')

    if (preco_promocional) {
        variation_preco_promocional.innerHTML = preco_promocional;
        variation_preco.classList.add('product-old-price')
        variation_preco.classList.add('text-muted')
        variation_preco.classList.remove('product-price')
    }
}

(function () {
    select_variacao = document.getElementById('select-variacoes');
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');

    if (!select_variacao) {
        return;
    }

    if (!variation_preco) {
        return;
    }

    url_params = new URLSearchParams(window.location.search);
    selected_vid = url_params.get('vid')
    if (selected_vid) {
        option = document.getElementById(`vid-${selected_vid}`);
        changePrices(option);
        url_params.set('vid', selected_vid)
        history.replaceState(null, null, '?' + url_params.toString());
    }

    select_variacao.addEventListener('change', function () {
        option = this.options[this.selectedIndex];
        changePrices(option);
        id = option.id.split('-')[1];
        url_params.set('vid', id)
        history.replaceState(null, null, '?' + url_params.toString());
    })
})();
