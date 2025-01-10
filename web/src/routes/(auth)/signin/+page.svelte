<script lang="ts">
  import { goto } from "$app/navigation";
  import { _ } from "svelte-i18n";

  $: email = '';
  $: password = '';

  let isInputFilled: boolean = false;
  
  $: {
    if (email && password) {
      isInputFilled = true;
    }
    else {
      isInputFilled = false;
    }
  }

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    
    try {
      const response = await fetch('http://localhost:2843/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
      });

      if (response.ok) {
        await goto('/');
      }
      else {
        console.error('Login failed');
      }
    }
    catch (error) {
      console.error('Login failed', error);
    }
  }
</script>


<svelte:head>
  <title>{$_('signin')} • mixel-music</title>
</svelte:head>

<div class="signin-form">
  <form on:submit={handleSubmit}>
    <input
      type="email"
      bind:value={email}
      placeholder={$_('email')}
      autocomplete="email"
      required
    />
    <input
      type="password"
      bind:value={password}
      placeholder={$_('password')}
      autocomplete="current-password"
      required
    />

    <button class="login-button" disabled={!isInputFilled} type="submit">
      {$_('signin')}
    </button>
  </form>
</div>

<style>
  .signin-form {
    display: flex;
    justify-content: space-evenly;
    flex-direction: column;
    background-color: var(--dark-content);
    padding: var(--space-sl);
    border-radius: var(--radius-m);
    box-shadow: 0 0 0 0.5px var(--dark-border) inset;
  }

  form {
    display: flex;
    gap: var(--space-m);
    flex-direction: column;
  }

  input {
    width: 360px;
    font-size: 15px;
    display: block;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-m);
    color: var(--dark-text);
    font-family: var(--font-family);
    padding: var(--space-s) calc(var(--space-s) + 2px);
    transition: all 0.2s ease;
    backdrop-filter: blur(32px);
  }

  .login-button {
    font-size: 15px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text);
    background-color: #211951;
    border: 1px solid var(--dark-border);
    transition: 0.2s ease;
    border-radius: var(--radius-m);
    font-weight: 500;
    padding: var(--space-s) calc(var(--space-s) + 2px);
    text-decoration: none;
  }

  .login-button:disabled {
    background-color: var(--black-3a);
  }
</style>
