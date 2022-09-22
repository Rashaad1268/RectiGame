<script lang="ts">
	import { faDiscord, faGithub, faYoutube } from '@fortawesome/free-brands-svg-icons';
	import FaIcon from 'svelte-fa';
</script>

<footer class="footer p-10 bg-base-300 text-base-content mt-10">
	<div>
		<span class="footer-title">Links</span>
		<a
			href="https://github.com/Rashaad1268/Gamerz.lk"
			target="_blank"
			class="flex items-center gap-1 link link-hover"><FaIcon icon={faGithub} /> Source code</a
		>
	</div>
	<div>
		<span class="footer-title">Social</span>
		<div class="grid grid-flow-col gap-4">
			<a href="https://discord.gg/PeKDHwcRE3" target="_blank"
				><FaIcon icon={faDiscord} size="3x" /></a
			>
			<a href="https://www.youtube.com/channel/UCV6UFqGfSHuWVph5BckMf9g" target="_blank"
				><FaIcon icon={faYoutube} size="3x" /></a
			>
		</div>
	</div>
</footer>

<style>
	footer {
		flex-shrink: 0;
	}
</style>
