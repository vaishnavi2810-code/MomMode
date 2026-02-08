import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, HeartPulse, Lock, Mail } from 'lucide-react'
import { apiRequest, API_PATHS, HTTP } from '../lib/api'

const LoginPage = () => {
  const [isLoading, setIsLoading] = useState(false)

  const BUTTON_LABEL = 'Sign in with Google'
  const BUTTON_LOADING_LABEL = 'Redirecting...'
  const AUTH_ERROR_MESSAGE = 'Unable to start Google sign-in.'

  const handleGoogleSignIn = async () => {
    setIsLoading(true)
    const result = await apiRequest<{ auth_url: string }>(API_PATHS.AUTH_GOOGLE_URL, {
      method: HTTP.GET,
    })
    setIsLoading(false)

    if (result.error || !result.data?.auth_url) {
      console.error(AUTH_ERROR_MESSAGE, result.error)
      return
    }

    window.location.assign(result.data.auth_url)
  }

  return (
    <div className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto max-w-md">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
            <HeartPulse className="h-5 w-5" />
          </div>
          <div>
            <p className="text-lg font-semibold text-slate-900">MomMode</p>
            <p className="text-xs text-slate-500">Doctor portal access</p>
          </div>
        </Link>

        <div className="mt-8 rounded-3xl border border-slate-200 bg-white p-8 shadow-soft">
          <h1 className="text-2xl font-semibold text-slate-900">Welcome back</h1>
          <p className="mt-2 text-sm text-slate-600">
            Sign in to manage your clinic&apos;s AI calling coverage.
          </p>

          <form className="mt-6 space-y-4">
            <label className="block text-sm font-semibold text-slate-700">
              Work email
              <div className="relative mt-2">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  type="email"
                  placeholder="doctor@clinic.com"
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm text-slate-700 outline-none transition focus:border-primary focus:bg-white"
                />
              </div>
            </label>
            <label className="block text-sm font-semibold text-slate-700">
              Password
              <div className="relative mt-2">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm text-slate-700 outline-none transition focus:border-primary focus:bg-white"
                />
              </div>
            </label>
            <button
              type="button"
              onClick={handleGoogleSignIn}
              className="flex w-full items-center justify-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
              disabled={isLoading}
            >
              {isLoading ? BUTTON_LOADING_LABEL : BUTTON_LABEL}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          <div className="mt-5 text-xs text-slate-500">Doctor-only access</div>
        </div>

        <div className="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white/60 px-6 py-4 text-xs text-slate-500">
          Need an account?{' '}
          <Link to="/signup" className="font-semibold text-primary">
            Create one
          </Link>{' '}
          to access your clinic workspace.
        </div>
      </div>
    </div>
  )
}

export default LoginPage
