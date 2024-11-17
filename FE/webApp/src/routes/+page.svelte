<script lang="ts">
    import { isAuthenticated, handleLogin } from '$lib/auth/auth-store';
    import { goto } from '$app/navigation';

    async function handleLoginClick() {
        try {
            console.log('Initiating login...');
            await handleLogin();
        } catch (error) {
            console.error('Login error:', error);
            goto('/login');
        }
    }
</script>


<div class="login-container">
    <!-- <h2>Welcome to</h2> -->

	<h1 class="titleFont">EasyTeller</h1>

	<div>
		<div class="loader">
		  <p>A new way to supply </p>
		  <div class="words">
			<span class="word">credit</span>
			<span class="word">loans</span>
			<span class="word">banking</span>
			<span class="word">savings</span>
			<span class="word">finances</span>
		  </div>
		</div>
	  </div>



    {#if !$isAuthenticated}
        <!-- From Uiverse.io by cssbuttons-io  -->
        <button class="learn-more" on:click={handleLoginClick}>
            <span class="circle" aria-hidden="true">
                <span class="icon arrow"></span>
            </span>
            <span class="button-text">Go to Login</span>
        </button>

        <!-- <button on:click={handleLoginClick}>Go to Login</button> -->
    {/if}
</div>

<style>

	@import url('https://fonts.googleapis.com/css2?family=Geist&family=Playfair+Display&display=swap');

	.titleFont {
	font-family: "Playfair Display", serif;
	font-optical-sizing: auto;
	font-weight: 400;
	font-style: normal;
	font-size: 12vh;
	}

    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        color: white;
        /* font-family: "Geist Sans"; */
    }


	/* --------------------------- Sliding promo */

.card {
  /* color used to softly clip top and bottom of the .words container */
  --bg-color: #212121;
  background-color: var(--bg-color);
  padding: 1rem 2rem;
  border-radius: 1.25rem;
}
.loader {
  color: rgb(124, 124, 124);
  font-family: "Poppins", sans-serif;
  font-weight: 500;
  font-size: 25px;
  -webkit-box-sizing: content-box;
  box-sizing: content-box;
  height: 40px;
  padding: 10px 10px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  border-radius: 8px;
}

.words {
  overflow: hidden;
  position: relative;
  top: 25px;
}
.words::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    var(--bg-color) 10%,
    transparent 30%,
    transparent 70%,
    var(--bg-color) 90%
  );
  z-index: 20;
}

.word {
  display: block;
  height: 100%;
  padding-left: 6px;
  color: white;
  animation: spin_4991 4s infinite;
}

@keyframes spin_4991 {
  10% {
    -webkit-transform: translateY(-102%);
    transform: translateY(-102%);
  }

  25% {
    -webkit-transform: translateY(-100%);
    transform: translateY(-100%);
  }

  35% {
    -webkit-transform: translateY(-202%);
    transform: translateY(-202%);
  }

  50% {
    -webkit-transform: translateY(-200%);
    transform: translateY(-200%);
  }

  60% {
    -webkit-transform: translateY(-302%);
    transform: translateY(-302%);
  }

  75% {
    -webkit-transform: translateY(-300%);
    transform: translateY(-300%);
  }

  85% {
    -webkit-transform: translateY(-402%);
    transform: translateY(-402%);
  }

  100% {
    -webkit-transform: translateY(-400%);
    transform: translateY(-400%);
  }
}


    /* --------------------------- Button 1 */
button {
	position: relative;
	top: 40px;
	display: inline-block;
	cursor: pointer;
	outline: none;
	border: 0;
	vertical-align: middle;
	text-decoration: none;
	background: transparent;
	padding: 0;
	font-size: inherit;
	font-family: inherit;
   }
   
   button.learn-more {
	width: 12rem;
	height: auto;
   }
   
   button.learn-more .circle {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: relative;
	display: block;
	margin: 0;
	width: 3rem;
	height: 3rem;
	background: #282936;
	border-radius: 1.625rem;
   }
   
   button.learn-more .circle .icon {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: absolute;
	top: 0;
	bottom: 0;
	margin: auto;
	background: #fff;
   }
   
   button.learn-more .circle .icon.arrow {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	left: 0.625rem;
	width: 1.125rem;
	height: 0.125rem;
	background: none;
   }
   
   button.learn-more .circle .icon.arrow::before {
	position: absolute;
	content: "";
	top: -0.29rem;
	right: 0.0625rem;
	width: 0.625rem;
	height: 0.625rem;
	border-top: 0.125rem solid #fff;
	border-right: 0.125rem solid #fff;
	transform: rotate(45deg);
   }
   
   button.learn-more .button-text {
	transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	padding: 0.75rem 0;
	margin: 0 0 0 1.85rem;
	color: #fff;
	font-weight: 700;
	line-height: 1.6;
	text-align: center;
	text-transform: uppercase;
   }
   
   button:hover .circle {
	width: 100%;
   }
   
   button:hover .circle .icon.arrow {
	background: #fff;
	transform: translate(1rem, 0);
   }
   
   button:hover .button-text {
	color: #fff;
   }
</style>