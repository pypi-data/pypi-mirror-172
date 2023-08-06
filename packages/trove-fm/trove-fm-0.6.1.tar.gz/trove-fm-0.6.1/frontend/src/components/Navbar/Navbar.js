
import React from "react"
import Button from 'react-bootstrap/Button';
// import { useAuthenticatedUser } from "hooks/auth/useAuthenticatedUser"
// import { UserAvatar } from "components"
import { Link, useNavigate } from "react-router-dom"
// import loginIcon from "assets/img/loginIcon.svg"

const AvatarMenu = <div></div>

export default function Navbar() {
  const navigate = useNavigate()
  const [avatarMenuOpen, setAvatarMenuOpen] = React.useState(false)
  // const { user, logUserOut } = useAuthenticatedUser()
  const user = {name: 'btf'}

  const toggleAvatarMenu = () => setAvatarMenuOpen(!avatarMenuOpen)

  const closeAvatarMenu = () => setAvatarMenuOpen(false)

  // const handleLogout = () => {
  //   closeAvatarMenu()
  //   logUserOut()
  //   navigate("/")
  // }

  const avatarButton = (
    <Button variant="primary" type="submit">avatarButton</Button>
  )

  const renderAvatarMenu = () => {
    if (!user?.profile) return null

    return (
      <AvatarMenu>
      </AvatarMenu>
    )
  }

  return (
    <div>
      <h3>Trove Farmers Market (Navbar goes here)</h3>
    </div>
  )
}
