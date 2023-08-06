# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uncertainty_loss']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'uncertainty-loss',
    'version': '0.1.1',
    'description': 'Uncertainty Loss functions for deep learning',
    'long_description': '# Uncertainty Loss \n*Loss functions for uncertainty quantification in deep learning.*\n\nThis package implements loss functions from the following papers\n\n* Evidential Deep Learning to Quantify Classification Uncertainty\n    * `ul.evidential_loss`\n* Information Aware Max-Norm Dirichlet Networks for Predictive Uncertainty Estimation\n    * `ul.maxnorm_loss`\n\n\n\nThese loss functions can be used as drop in replacements for \n`torch.nn.functional.cross_entropy`.  See QuickStart and Examples below.\n\n## Quickstart \nInstall the package with pip\n```bash\npip install uncertainty-loss\n```\nThen use the loss in a training pipeline. For example:\n```python\nimport uncertainty_loss as ul\nimport torch \n\ndef fit_step(model, x, targets, reg_factor=0):\n    """Runs a single training step and retuns the loss for the batch.\n\n    Note the inputs to the uncertainty loss function need to be \n    non-negative.  Any transformation will work (exp, relu, softplus,\n    etc) but we have found that exp works best (in agreement with the \n    original papers).  For convenience we provide a clamped exp function\n    to avoid overflow.\n    """\n    logits = model(x)\n    evidence = ul.clamped_exp(logits) # non-negative transform\n    loss = ul.maxnorm_loss(evidence, targets, reg_factor)\n    return loss\n```\n\n\n### Examples\nReplace \n```python\nfrom torch.nn import functional as F\n\nloss = F.cross_entropy(x,y)\n```\nWith\n```python\nimport uncertainy_loss as ul\n\nloss = ul.evidential_loss(x,y)\n# or \nloss = ul.maxnorm_loss(x,y)\n```\n\nThe loss functions also accept a reduction parameter with the same\nproperties as the `cross_entropy` loss.\n\n#### Important\nFor each loss function is a regularization term that is shown to be \nbeneficial for learning to quantify uncertainty.  In practice, \nto ensure that the regularization term does not dominate early \nin training, we ramp up the regularization term from 0 to a max factor\ne.g. 0->1.  It is up to the user to ensure this happens.  Each loss \nfunction takes an additional parameter `reg_factor`.  During training \none can increment `reg_factor` to accomplish this ramp up.  By \ndefault `reg_factor==0` so there is no regularization unless \nexplicitly "turned on"\n\n### Example with Regularization Annealing\n```python\nimport uncertainty_loss as ul\n\nreg_steps = 1000\nreg_step_size = 1/reg_steps\nreg_factor = 0\nfor epoch in range(epochs):\n\n    for x,y in dataloader:\n        logits = model(x)\n        evidence = ul.clamped_exp(logits)\n        loss = ul.maxnorm_loss(evidence, y, reg_factor=reg_factor)\n        reg_factor = min(reg_factor+reg_step_size, 1)\n```\n\n\n## Motivation\nUncertainty quantification has important applications in AI Safety and active learning.  Neural networks trained with a traditional cross entropy loss are often over-confident in unfamiliar situations.  It\'s easy to see why this can be disastrous: An AI surgeon making a confident but wrong incision in an unfamilar situation, a self-driving car making a confident but wrong turn, an AI investor making a confident but wrong buy/sell decision.\n\nThere have been several methods proposed for uncertainty quantification.  Many of the popular methods require specific network architectures (e.g. Monte Carlo Dropout requires dropout layers) or require expensive inference (Monte Carlo dropout requires multiple runs through the same model, ensemble methods require multiple models). \n\nRecently methods for uncertainty quantification have been proposed that do not require any changes to the network architecture and have no inference overhead.  Instead they propose to learn parameters of a "higher order distribution" and use this distribution to quantify the uncertainty in the prediction.  They have been shown to be effective.\n\nUnfortunately, these methods haven\'t been integrated into any of the main deep learning packages and the heavy math makes the implementation a bit tricky.  \n\nFor these reasons we have created the `uncertainty-loss` package.',
    'author': 'Mike Vaiana',
    'author_email': 'mike@ae.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
