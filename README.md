# Spotify-Skip-Checker

<h2>But Why?</h2>
<p>Do you find yourself skipping songs in your spotify playlists but never getting the courage to remove it
 from your playlist in fear you might want to listen to it again?</p>
 <br?
 <p>This is the exact problem I've come to solve.</p>

<h2>So what actually is it and what does it do?</h2>
<p>With this application it will track the playlist the song is in and will attempt to track the number of times it's been skipped. Once this song has been skipped x amount of times it will be removed from the current playlist and will be moved into a new playlist (This is so we know what songs have been removed).</p>

<h2>But how are you doing this?</h2>
Using my minimal knowledge of the Spotipy (yep, that's how it's spelt) and the help of 2 trusty friends, Python and Sqlite, I will be creating this. The main plan is to use some sort of counter to track each song played, insert those into a database and using Spotipy track the total number of skips...
<br>
I wish it was this easy, turns out Spotipy doesn't come with an inbuilt feature to check for "total skips" each track has. So to work around this currently the main goal is to create a variable, let's say `currentSong`, and assign the song name to this. And every 10 seconds for 3 iterations, compare the value in `currentSong` to the actual current song playing. If not the same we can assume that the song has been skipped, therefore add +1 to the `skippedSongCount` in the database

<h2>How do I use this?</h2>
Good question, let me attempt building this, then I'll get back to you :)
