import NextAuth from 'next-auth';
import GithubProvider from 'next-auth/providers/github';

const handler = NextAuth({
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_CLIENT_ID ?? 'missing',
      clientSecret: process.env.GITHUB_CLIENT_SECRET ?? 'missing'
    })
  ],
  session: {
    strategy: 'jwt'
  }
});

export { handler as GET, handler as POST };
